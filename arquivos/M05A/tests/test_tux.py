"""
Testes do Tux: ele só existe quando o jogo roda no Linux.

O sys.platform diz para que sistema o Python foi feito, e o teste não pode
depender da máquina em que roda. A fixture monkeypatch do pytest troca um
valor só durante o teste ("finge" outro sistema) e desfaz a troca no fim.
"""
import sys

from src.controllers import npcs_do_sistema


def test_tux_aparece_no_linux(monkeypatch):
    monkeypatch.setattr(sys, "platform", "linux")  # finge que o Python é do Linux

    npcs = npcs_do_sistema()

    assert [npc.sprite_id for npc in npcs] == ["tux"]


def test_tux_nao_aparece_fora_do_linux(monkeypatch):
    # TODO: finja o Windows ("win32") e o macOS ("darwin") com o monkeypatch, como no teste
    #       de cima, e afirme que npcs_do_sistema() devolve a lista vazia nos dois.
    assert False, "TODO: escreva o teste"
