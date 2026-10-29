"""
Teste da conversa: o Controller pede a fala, o serviço de IA falso responde.

Sem rede e sem cota: o falso entra no lugar do Gemini pela mesma porta que o
main.py usa (injeção de dependências), e anota o que o jogo pediu.
"""
from src.controllers import Controle
from src.models import Estado


def test_conversa_usa_o_servico_de_ia(jogo, tela, ia_falsa):
    controle = Controle(jogo, tela, ia_falsa)  # o falso no lugar do ServicoIA
    mago = jogo.cena.npcs[0]
    controle.conversar(mago, "Bom dia, mestre.")
    jogo.mudar_estado(Estado.DIALOGO)
    controle.dialogo.avancar()  # "Pensando..." aparece inteiro de uma vez
    controle.atualizar(0.016)  # um quadro: é nele que o Controller chama a IA

    # Pediu uma vez só, com a persona do mago e a fala do jogador.
    assert ia_falsa.pedidos == [(mago.instrucao, "Bom dia, mestre.")]
    # A caixa de diálogo mostra a resposta do falso, e ninguém mais está esperando.
    assert controle.dialogo.paginas[0][0] == "Fala de teste."
    assert controle.pedindo is None
