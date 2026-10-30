"""
Testes das conquistas: os eventos entram, a ConquistaDesbloqueada sai (uma vez só).
"""
from src.conquistas import Conquistas
from src.eventos import CenaAlterada, ConquistaDesbloqueada, EventBus, ItemRecebido


def montar():
    """Um EventBus com as conquistas assinando e uma lista com o que elas publicam."""
    eventos = EventBus()
    conquistas = Conquistas(eventos)
    desbloqueadas = []
    eventos.assinar(ConquistaDesbloqueada, desbloqueadas.append)
    return eventos, conquistas, desbloqueadas


def test_explorador_ao_entrar_na_floresta():
    eventos, conquistas, desbloqueadas = montar()
    eventos.publicar(CenaAlterada("salao", "floresta"))
    assert conquistas.obtidas == ["explorador"]
    assert desbloqueadas == [ConquistaDesbloqueada("explorador", "Explorador", "floresta")]


def test_explorador_uma_vez_so():
    eventos, conquistas, desbloqueadas = montar()
    eventos.publicar(CenaAlterada("salao", "floresta"))
    eventos.publicar(CenaAlterada("floresta", "salao"))
    eventos.publicar(CenaAlterada("salao", "floresta"))  # voltou: nada de novo
    assert len(desbloqueadas) == 1


def test_outras_cenas_nao_contam():
    eventos, conquistas, _ = montar()
    eventos.publicar(CenaAlterada("floresta", "masmorra"))
    assert "explorador" not in conquistas.obtidas


def test_portador_da_chave():
    eventos, conquistas, _ = montar()
    eventos.publicar(ItemRecebido("Poção de velocidade", "floresta"))
    assert conquistas.obtidas == []
    eventos.publicar(ItemRecebido("Chave da Masmorra", "salao"))
    assert conquistas.obtidas == ["portador_da_chave"]
