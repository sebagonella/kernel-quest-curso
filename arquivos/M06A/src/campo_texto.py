"""
RPG Engine — o campo de texto da conversa (parte da View).

Guarda o que o jogador está digitando e desenha a linha "Sua vez" logo acima
da caixa de diálogo, com um cursor piscando. Quem decide quando o campo
recebe letras e quando a frase é enviada é o Controller: aqui só se guarda e
se desenha.
"""
import pygame

from src.config import COR_APAGADA, COR_DESTAQUE, COR_PAINEL, COR_TEXTO, PISCA_POR_SEGUNDO

LIMITE_CARACTERES = 80  # uma frase curta: cabe na linha e economiza tokens


class CampoTexto:
    """Uma linha de texto editável: digitar, apagar, limpar e desenhar."""

    def __init__(self, limite=LIMITE_CARACTERES):
        self.texto = ""
        self.limite = limite

    def digitar(self, letras):
        """Acrescenta o que chegou num evento TEXTINPUT (já com acento), até o limite."""
        if not self.texto:
            letras = letras.lstrip()  # o ESPAÇO que completou a fala não vira texto
        self.texto = (self.texto + letras)[:self.limite]

    def apagar(self):
        """BACKSPACE: tira a última letra."""
        self.texto = self.texto[:-1]

    def limpar(self):
        """Devolve o texto digitado e deixa o campo vazio para a próxima frase."""
        texto, self.texto = self.texto.strip(), ""
        return texto

    def desenhar(self, tela, fonte, x, base, largura, tempo):
        """A faixa "Sua vez:" com o texto e o cursor, de largura `largura`, terminando em `base`."""
        altura = fonte.get_height() + 8
        fundo = pygame.Surface((largura, altura), pygame.SRCALPHA)
        fundo.fill(COR_PAINEL)
        topo = base - altura
        tela.blit(fundo, (x, topo))
        rotulo = fonte.render("Sua vez:", False, COR_DESTAQUE)
        tela.blit(rotulo, (x + 12, topo + 4))
        inicio = x + 24 + rotulo.get_width()
        if self.texto:
            imagem = fonte.render(self.texto, False, COR_TEXTO)
        else:  # vazio: uma dica apagada no lugar do texto
            imagem = fonte.render("digite e aperte ENTER (vazio: encerra)", False, COR_APAGADA)
        # Texto maior que a faixa: mostra só o final, onde o cursor está.
        sobra = max(imagem.get_width() - (largura - (inicio - x) - 24), 0)
        tela.blit(imagem, (inicio, topo + 4), area=pygame.Rect(sobra, 0, imagem.get_width(), altura))
        if int(tempo * PISCA_POR_SEGUNDO) % 2 == 0:  # o cursor pisca no fim do texto
            cursor_x = inicio + (imagem.get_width() - sobra if self.texto else 0)
            pygame.draw.rect(tela, COR_TEXTO, (cursor_x + 2, topo + 6, 3, altura - 12))
        return topo
