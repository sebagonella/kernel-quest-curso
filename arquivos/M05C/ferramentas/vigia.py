"""
A Vigia: conta quem tentou entrar pelo SSH e grava o Quadro da Vigia do jogo.

Lê um auth.log (o de exemplo, ferramentas/auth.log.exemplo, ou o da sua máquina),
acha cada tentativa de entrar com um usuário que não pode entrar e grava em
assets/dados/invasores.json o que o Quadro mostra: o total de tentativas, quantos
IPs diferentes tentaram (só o número) e os 5 usuários mais tentados.

Uso:
    python ferramentas/vigia.py                       # o log de exemplo
    python ferramentas/vigia.py /var/log/auth.log     # o log da sua máquina

Os nomes vêm de quem atacou: são entrada controlada por um desconhecido. Por isso
o vigia corta cada nome em 16 caracteres e mantém só letras, números, _ e -, e o
JSON nunca guarda IPs (são de terceiros).
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

PASTA_PROJETO = Path(__file__).resolve().parent.parent
LOG_EXEMPLO = PASTA_PROJETO / "ferramentas" / "auth.log.exemplo"
SAIDA = PASTA_PROJETO / "assets" / "dados" / "invasores.json"

# As duas linhas que o sshd grava quando alguém tenta um usuário que não pode entrar:
#   "Invalid user admin from 203.0.113.7 port 51234"            (o usuário não existe)
#   "User root from 203.0.113.7 not allowed because not listed in AllowUsers"  (existe, mas não pode)
# A data no começo da linha não importa (no Ubuntu 24.04 ela vem no formato ISO 8601).
TENTATIVA = re.compile(r"(?:Invalid user (.*) from (\S+) port \d+$"
                       r"|User (.*) from (\S+) not allowed because)")
MAXIMO_NOME = 16
PROIBIDO = re.compile(r"[^A-Za-z0-9_-]")  # tudo o que não é letra, número, _ ou -


def sanear(nome):
    """Um nome que veio de um atacante, seguro para mostrar: só A-Z, 0-9, _ e -, até 16."""
    limpo = PROIBIDO.sub("", nome)[:MAXIMO_NOME]
    return limpo or "?"  # nome vazio (ou só com símbolos) vira "?"


def ler_tentativas(linhas):
    """[(usuário saneado, ip)], uma por tentativa, na ordem do log."""
    tentativas = []
    for linha in linhas:
        achou = TENTATIVA.search(linha.rstrip())
        if achou:
            usuario, ip = achou.group(1, 2) if achou.group(2) else achou.group(3, 4)
            tentativas.append((sanear(usuario), ip))
    return tentativas


def resumir(tentativas, quantos=5):
    """O que o Quadro mostra: números e nomes, nunca os IPs."""
    # TODO 1: os `quantos` usuários mais tentados, do mais tentado para o menos, numa lista de
    #         {"usuario": nome, "tentativas": vezes}. Dica: Counter(...) conta quantas vezes
    #         cada valor aparece, e .most_common(quantos) devolve os pares (valor, vezes) em ordem.
    mais_tentados = []  # TODO 1
    # TODO 2: quantos IPs diferentes tentaram (só o número; os IPs não vão para o JSON).
    #         Dica: um set guarda cada valor uma vez só.
    ips_distintos = 0  # TODO 2
    return {"total_tentativas": len(tentativas), "ips_distintos": ips_distintos,
            "mais_tentados": mais_tentados}


def main():
    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else LOG_EXEMPLO
    # errors="replace": um byte estranho no log (de um atacante) não derruba a leitura.
    linhas = caminho.read_text(encoding="utf-8", errors="replace").splitlines()
    resumo = resumir(ler_tentativas(linhas))
    resumo["fonte"] = caminho.name  # só o nome do arquivo, sem a pasta
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(json.dumps(resumo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{resumo['total_tentativas']} tentativas de {resumo['ips_distintos']} IPs -> {SAIDA}")
    for linha in resumo["mais_tentados"]:
        print(f"  {linha['tentativas']:4}  {linha['usuario']}")


if __name__ == "__main__":
    main()
