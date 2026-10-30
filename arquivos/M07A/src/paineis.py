"""
RPG Engine — o que a IA muda na tela (parte da View, desde o M06B).

O balão de emoção acima do NPC, o "pensando" (M07A), o painel "Receber" de um
item e a boca do portão aberta. Como o depuracao.py, só LÊ: recebe a Tela (para usar as fontes,
o painel e o cache de ícones dela) e desenha. Quem decide o que aparece é o
Controller (a emoção da fala) e o Model (a oferta, o portão).
"""
import math

import pygame

from src.config import COR_APAGADA, COR_DESTAQUE, COR_FAIXA, COR_TEXTO, LARGURA

TAMANHO_BALAO = 42  # o balão do pacote tem 14×13 pixels: 3× cabe em 42
COR_BOCA = (18, 16, 24)  # o escuro da boca da masmorra, sem a grade


def desenhar_balao(tela, npc, emocao, camera_x, camera_y):
    """O balão da emoção logo acima da cabeça do NPC; sem emoção, nada."""
    if emocao is None:
        return
    balao = tela.icone(f"interface/emocao_{emocao}.png", TAMANHO_BALAO)
    base = (npc.caixa.centro[0] - camera_x, npc.caixa.y - camera_y + 6)
    tela.superficie.blit(balao, balao.get_rect(midbottom=base))


def desenhar_pensando(tela, cena, aguardando, tempo, camera_x, camera_y):
    """O balão de reticências, subindo e descendo, acima de cada NPC que espera a IA."""
    balao = tela.icone("interface/emocao_pensativo.png", TAMANHO_BALAO)
    for npc in cena.npcs:
        if npc.nome in aguardando:
            sobe = round(math.sin(tempo * 6) * 4)  # a animação mostra que o jogo não parou
            base = (npc.caixa.centro[0] - camera_x, npc.caixa.y - camera_y + 6 + sobe)
            tela.superficie.blit(balao, balao.get_rect(midbottom=base))


def desenhar_receber(tela, item):
    """O painel "Receber": ícone, nome e descrição do item, e o botão de confirmar."""
    superficie = tela.superficie
    painel = pygame.Surface((420, 230), pygame.SRCALPHA)
    painel.fill(COR_FAIXA)
    x, y = (LARGURA - painel.get_width()) // 2, 170  # abaixo do NPC e do balão
    superficie.blit(painel, (x, y))
    centro = LARGURA // 2
    titulo = tela.fonte.render("Você recebe", False, COR_APAGADA)
    superficie.blit(titulo, titulo.get_rect(center=(centro, y + 26)))
    icone = tela.icone(item.imagem, 72)
    superficie.blit(icone, icone.get_rect(center=(centro, y + 82)))
    nome = tela.fonte.render(item.nome, False, COR_DESTAQUE)
    superficie.blit(nome, nome.get_rect(center=(centro, y + 132)))
    descricao = tela.fonte_fala.render(item.descricao, False, COR_TEXTO)
    superficie.blit(descricao, descricao.get_rect(center=(centro, y + 162)))
    botao = tela.fonte.render("[ ENTER  Receber ]", False, COR_DESTAQUE)
    superficie.blit(botao, botao.get_rect(center=(centro - 60, y + 202)))
    recusar = tela.fonte_fala.render("ESC recusar", False, COR_APAGADA)
    superficie.blit(recusar, recusar.get_rect(center=(centro + 140, y + 202)))


def desenhar_portao(tela, portao, camera_x, camera_y):
    """Portão aberto: a grade some, e fica só a boca escura da masmorra."""
    if portao is None or not portao.aberto:
        return
    caixa = portao.caixa
    pygame.draw.rect(tela.superficie, COR_BOCA,
                     (caixa.x - camera_x, caixa.y - camera_y, caixa.largura, caixa.altura))
