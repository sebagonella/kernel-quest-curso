"""
RPG Engine — o log de auditoria: um assinante que grava tudo (desde o M07B).

Cada evento vira uma linha JSON no auditoria.log: o que aconteceu, quando e com
quais dados. O log do terminal é para quem depura agora; a auditoria responde
depois "o que aconteceu nesta partida?". Gravar um arquivo pequeno é rápido, por
isso este assinante não precisa de thread, ao contrário do Discord.
"""
import json
from dataclasses import asdict
from datetime import datetime

from src.eventos import CenaAlterada, ConquistaDesbloqueada, ItemRecebido, NPCInteragido

TIPOS = (CenaAlterada, NPCInteragido, ItemRecebido, ConquistaDesbloqueada)


class Auditoria:
    """Assina todos os tipos de evento e grava cada um numa linha do arquivo."""

    def __init__(self, eventos, arquivo):
        self.arquivo = arquivo
        for tipo in TIPOS:
            eventos.assinar(tipo, self.registrar)

    def registrar(self, evento):
        # asdict() transforma o evento (uma dataclass) num dicionário com os campos dele.
        linha = {"quando": datetime.now().isoformat(timespec="seconds"),
                 "evento": type(evento).__name__, **asdict(evento)}
        with open(self.arquivo, "a", encoding="utf-8") as arquivo:  # "a": acrescenta no fim
            arquivo.write(json.dumps(linha, ensure_ascii=False) + "\n")
