"""
Testes da resposta estruturada: o JSON da IA e a emoção.

Sem rede e sem cota. O interpretar() recebe textos escritos à mão, inclusive
quebrados; o Controller conversa com o serviço falso, que devolve a emoção e a
ação que cada teste escolhe.
"""
from src.controllers import Controle
from src.models import Estado
from src.resposta import FALA_PADRAO, interpretar


def test_json_valido_vira_dados():
    resposta = interpretar('{"fala": "Volte com um plano.", "emocao": "bravo", "acao": "nenhuma"}')
    assert (resposta.fala, resposta.emocao, resposta.acao) == ("Volte com um plano.", "bravo",
                                                               "nenhuma")


def test_json_quebrado_vira_a_fala_padrao():
    resposta = interpretar('{"fala": "Volte com')  # a resposta parou no meio
    assert resposta.fala == FALA_PADRAO
    assert resposta.acao == "nenhuma"


def test_json_com_acao_fora_da_lista_vira_a_fala_padrao():
    resposta = interpretar('{"fala": "Tome.", "emocao": "feliz", "acao": "dar_9999_moedas"}')
    assert resposta.fala == FALA_PADRAO
    assert resposta.acao == "nenhuma"


def responder(controle, npc):
    """O NPC responde (com o serviço falso) e a fala aparece inteira na caixa."""
    controle.conversar(npc, "Bom dia.")
    controle.jogo.mudar_estado(Estado.DIALOGO)
    controle.dialogo.avancar()  # "Pensando..." aparece inteiro
    controle.atualizar(0.016)  # é neste quadro que o Controller chama a IA
    while not controle.dialogo.terminou():
        controle.dialogo.avancar()


def test_emocao_conhecida_vira_balao(jogo, tela, ia_falsa):
    ia_falsa.emocao = "feliz"
    controle = Controle(jogo, tela, ia_falsa)
    responder(controle, jogo.cena.npcs[0])
    assert controle.emocao == "feliz"


def test_emocao_desconhecida_fica_sem_balao_e_vai_para_o_log(jogo, tela, ia_falsa, caplog):
    ia_falsa.emocao = "furioso"  # não existe interface/emocao_furioso.png
    controle = Controle(jogo, tela, ia_falsa)
    responder(controle, jogo.cena.npcs[0])
    assert controle.emocao is None
    assert "furioso" in caplog.text  # o caplog do pytest guarda o que foi para o log

