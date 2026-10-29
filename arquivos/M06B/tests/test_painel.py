"""
Teste do painel "Receber": a Chave oferecida só entra no inventário com o ENTER.

Sem rede e sem cota: o serviço falso faz o papel do Mago que entrega a Chave
(a ação dar_item). O teste confere o estado do jogo antes e depois da confirmação.
"""
import pygame

from src.controllers import Controle
from src.models import CHAVE, Estado


def test_dar_item_abre_o_painel_e_so_o_receber_poe_no_inventario(jogo, tela, ia_falsa):
    mago = jogo.cena.npcs[0]
    mago.acoes_ia = ["dar_item"]  # este mago pode entregar a Chave...
    jogo.heroi.missao_aceita = True  # ...e o aprendiz já aceitou a missão
    ia_falsa.acao = "dar_item"
    controle = Controle(jogo, tela, ia_falsa)
    controle.conversar(mago, "Aceito a missão.")
    jogo.mudar_estado(Estado.DIALOGO)
    controle.dialogo.avancar()  # "Pensando..." aparece inteiro
    controle.atualizar(0.016)  # é neste quadro que o Controller chama a IA
    while not controle.dialogo.terminou():
        controle.dialogo.avancar()
    controle.atualizar(0.016)  # a fala terminou: o painel aparece no quadro seguinte

    assert jogo.estado == Estado.RECEBER
    assert jogo.oferta == CHAVE
    assert CHAVE not in jogo.heroi.inventario  # oferecida, mas ainda não recebida

    controle.tratar_evento(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
    assert CHAVE in jogo.heroi.inventario
    assert jogo.estado == Estado.DIALOGO


def test_sair_antes_do_fim_da_fala_cancela_a_oferta(jogo, tela, ia_falsa):
    mago = jogo.cena.npcs[0]
    mago.acoes_ia = ["dar_item"]
    jogo.heroi.missao_aceita = True
    ia_falsa.acao = "dar_item"
    controle = Controle(jogo, tela, ia_falsa)
    controle.conversar(mago, "Aceito a missão.")
    jogo.mudar_estado(Estado.DIALOGO)
    controle.dialogo.avancar()
    controle.atualizar(0.016)  # a IA responde: o painel espera o fim da fala
    controle.tratar_evento(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))  # sai antes

    ia_falsa.acao = "nenhuma"  # a conversa seguinte, com outro NPC, não sugere nada
    controle.conversar(mago, "Bom dia.")
    jogo.mudar_estado(Estado.DIALOGO)
    controle.dialogo.avancar()
    controle.atualizar(0.016)
    while not controle.dialogo.terminou():
        controle.dialogo.avancar()
    controle.atualizar(0.016)
    assert jogo.estado == Estado.DIALOGO  # nenhum painel pendurado da conversa anterior
    assert jogo.oferta is None
