"""
Testes do EventBus: assinar(tipo, funcao) e publicar(evento).

O EventBus é Python puro, sem pygame nem rede: os testes publicam eventos e
conferem quem recebeu. No fim, o Jogo publicando de verdade e a auditoria.
"""
import json

from src.auditoria import Auditoria
from src.eventos import CenaAlterada, EventBus, ItemRecebido, NPCInteragido
from src.models import Estado


def test_quem_assina_recebe_o_evento():
    eventos = EventBus()
    recebidos = []
    eventos.assinar(CenaAlterada, recebidos.append)  # qualquer função de um argumento serve
    eventos.publicar(CenaAlterada("salao", "floresta"))
    assert recebidos == [CenaAlterada("salao", "floresta")]


def test_so_chega_o_tipo_assinado():
    eventos = EventBus()
    recebidos = []
    eventos.assinar(ItemRecebido, recebidos.append)
    eventos.publicar(CenaAlterada("salao", "floresta"))  # ninguém assinou este tipo
    assert recebidos == []


def test_varios_assinantes_na_ordem():
    eventos = EventBus()
    ordem = []
    eventos.assinar(NPCInteragido, lambda evento: ordem.append("primeiro"))
    eventos.assinar(NPCInteragido, lambda evento: ordem.append("segundo"))
    eventos.publicar(NPCInteragido("Mercador Brok", "floresta"))
    assert ordem == ["primeiro", "segundo"]


def test_publicar_sem_assinantes_nao_faz_nada():
    EventBus().publicar(CenaAlterada("salao", "floresta"))  # não pode dar erro


def test_o_jogo_publica_a_troca_de_cena(jogo):
    recebidos = []
    jogo.eventos.assinar(CenaAlterada, recebidos.append)
    jogo.indo_para = "floresta"
    jogo.mudar_estado(Estado.TRANSICAO)
    jogo.atualizar_transicao(1.0)  # um dt grande: a tela fica preta e o mapa troca
    assert recebidos == [CenaAlterada("salao", "floresta")]


def test_auditoria_grava_uma_linha_por_evento(tmp_path):
    eventos = EventBus()
    arquivo = tmp_path / "auditoria.log"  # tmp_path: uma pasta temporária só deste teste
    Auditoria(eventos, arquivo)
    eventos.publicar(CenaAlterada("salao", "floresta"))
    eventos.publicar(NPCInteragido("Mercador Brok", "floresta"))
    linhas = [json.loads(linha) for linha in arquivo.read_text(encoding="utf-8").splitlines()]
    assert [linha["evento"] for linha in linhas] == ["CenaAlterada", "NPCInteragido"]
    assert linhas[1]["npc"] == "Mercador Brok"
