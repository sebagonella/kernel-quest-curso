"""
Testes do aviso no Discord, sem rede: o httpx.MockTransport faz o papel do Discord.

O Discord falso é uma função que recebe a requisição e devolve a resposta que
quisermos: 204 (aceito), 429 (devagar) ou 500. Nenhum teste sai da máquina.
"""
import json
import time

import httpx

from src.discord import NotificacaoDiscord
from src.eventos import ConquistaDesbloqueada, EventBus

URL = "https://discord.invalid/api/webhooks/1/teste"  # .invalid: um domínio que nunca existe


def discord_falso(*respostas):
    """Um cliente httpx que responde, em ordem, com os códigos dados; guarda as requisições."""
    pedidos = []
    fila = list(respostas)

    def responder(requisicao):
        pedidos.append(requisicao)
        codigo, cabecalhos = fila.pop(0) if len(fila) > 1 else fila[0]  # o último se repete
        return httpx.Response(codigo, headers=cabecalhos)

    return httpx.Client(transport=httpx.MockTransport(responder)), pedidos


def test_sem_url_fica_desligado():
    eventos = EventBus()
    discord = NotificacaoDiscord(eventos, "")
    assert not discord.ligado
    assert eventos.assinantes == {}  # nem assinou: publicar não chega a ele
    eventos.publicar(ConquistaDesbloqueada("explorador", "Explorador", "floresta"))


def test_envia_um_post_com_corpo_json():
    cliente, pedidos = discord_falso((204, {}))
    discord = NotificacaoDiscord(EventBus(), URL, cliente)
    assert discord.enviar("Teste")
    assert pedidos[0].method == "POST"
    assert json.loads(pedidos[0].content)["content"] == "Teste"


def test_429_espera_o_retry_after_e_tenta_de_novo():
    cliente, pedidos = discord_falso((429, {"Retry-After": "0.2"}), (204, {}))
    discord = NotificacaoDiscord(EventBus(), URL, cliente)
    inicio = time.perf_counter()
    assert discord.enviar("Teste")  # a segunda tentativa passou
    assert len(pedidos) == 2
    assert time.perf_counter() - inicio >= 0.2  # esperou o que o Discord pediu


def test_429_sem_fim_desiste():
    cliente, pedidos = discord_falso((429, {"Retry-After": "0"}))
    discord = NotificacaoDiscord(EventBus(), URL, cliente)
    assert not discord.enviar("Teste")
    assert len(pedidos) == 3  # TENTATIVAS_DISCORD, e não para sempre


def test_erro_do_servidor_nao_insiste():
    cliente, pedidos = discord_falso((500, {}))
    discord = NotificacaoDiscord(EventBus(), URL, cliente)
    assert not discord.enviar("Teste")
    assert len(pedidos) == 1


def test_a_conquista_chega_ao_discord_pela_thread():
    eventos = EventBus()
    cliente, pedidos = discord_falso((204, {}))
    NotificacaoDiscord(eventos, URL, cliente)
    eventos.publicar(ConquistaDesbloqueada("explorador", "Explorador", "floresta"))
    fim = time.perf_counter() + 2
    while not pedidos and time.perf_counter() < fim:  # a thread envia; esperamos até 2 s
        time.sleep(0.01)
    assert "Explorador" in json.loads(pedidos[0].content)["content"]
