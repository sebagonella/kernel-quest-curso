"""
Planta um bug escondido numa regra do jogo (src/models.py), para você caçar com um teste.

Sorteia um entre alguns bugs possíveis, muda uma linha do models.py sem dizer
qual, faz o commit dessa mudança e guarda a resposta em ferramentas/saida/
(pasta fora do Git). O jogo continua abrindo: o bug só aparece quando a regra
é usada do jeito certo.

Uso (da raiz do projeto, com a venv ativa):
    python ferramentas/plantar_bug.py            # planta (exige o models.py sem mudanças no Git)
    python ferramentas/plantar_bug.py --dica     # uma dica de onde procurar, sem entregar o bug
    python ferramentas/plantar_bug.py --revelar  # mostra qual foi (use depois de corrigir)

Não abra o arquivo da resposta nem olhe o último commit (git show) antes de
escrever o teste: o exercício é o teste encontrar o bug. Depois de corrigir,
git diff src/models.py mostra a sua correção.
"""
import argparse
import json
import random
import re
import shutil
import subprocess
import sys
from pathlib import Path

PASTA_PROJETO = Path(__file__).resolve().parent.parent
MODELS = PASTA_PROJETO / "src" / "models.py"
RESPOSTA = PASTA_PROJETO / "ferramentas" / "saida" / "bug_plantado.json"

# Cada bug: um padrão que precisa existir no models.py e o que entra no lugar dele.
# Os padrões miram trechos que todo projeto do curso tem iguais (ou quase) desde o M03C.
BUGS = [
    {
        "nome": "moeda que fica no chão",
        "padrao": r"self\.cena\.moedas\.remove\(moeda\)",
        "troca": "self.cena.moedas.count(moeda)",
        "dica": "Algo acontece com uma moeda depois que o herói a pega. Ou deveria acontecer.",
        "sintoma": "coletar_moedas() soma na bolsa, mas não tira a moeda do chão: "
                   "parado em cima dela, o herói a pega de novo a cada quadro.",
    },
    {
        "nome": "poção que dura demais",
        "padrao": r"self\.heroi\.pressa - dt, 0\.0",
        "troca": "self.heroi.pressa - dt / 10, 0.0",
        "dica": "A poção tem prazo. Será que o tempo passa no ritmo certo?",
        "sintoma": "passar_tempo() desconta só um décimo do dt: a poção de 10 segundos "
                   "dura 100.",
    },
    {
        "nome": "poção que não se gasta",
        "padrao": r"(\w+(?:\.heroi)?\.inventario)\.remove\(POCAO\)",
        "troca": r"\1.count(POCAO)",
        "dica": "Beber uma poção tem um custo. Confira se ele é cobrado.",
        "sintoma": "beber_pocao() liga a pressa, mas não tira a poção do inventário: "
                   "uma poção só dá para beber para sempre.",
    },
    {
        "nome": "item único comprado duas vezes",
        "padrao": r"item\.unico and item in ([\w.]+)",
        "troca": r"item.unico and \1.count(item) > 1",
        "dica": "Alguns itens só podem existir uma vez na bolsa. Tente comprar um deles duas "
                "vezes.",
        "sintoma": "comprar() só recusa um item único quando já há DOIS dele no inventário: "
                   "a armadura (ou o amuleto) sai duas vezes.",
    },
]


def sem_mudancas_no_git():
    """True se o models.py está igual ao último commit (dá para comparar depois com git diff)."""
    r = subprocess.run(["git", "status", "--porcelain", "--", str(MODELS)],
                       cwd=PASTA_PROJETO, capture_output=True, text=True)
    return r.returncode == 0 and not r.stdout.strip()


def plantar():
    if RESPOSTA.exists():
        print("Já existe um bug plantado. Ache-o com um teste e corrija; depois use --revelar.")
        return 1
    if not sem_mudancas_no_git():
        print("O src/models.py tem mudanças sem commit. Faça o commit antes de plantar o bug:")
        print("assim, depois de corrigir, o git diff mostra exatamente o que mudou.")
        return 1
    texto = MODELS.read_text(encoding="utf-8")
    possiveis = [bug for bug in BUGS if len(re.findall(bug["padrao"], texto)) == 1]
    if not possiveis:
        print("Nenhum dos bugs combina com o seu models.py. Peça ao Sênior que plante um à mão.")
        print("Sem mentor? Escreva mesmo assim os testes das regras de moeda, poção e compra:")
        print("o desafio vale com um teste seu para uma regra que ainda não tinha teste.")
        return 1
    bug = random.choice(possiveis)
    MODELS.write_text(re.sub(bug["padrao"], bug["troca"], texto), encoding="utf-8")
    # O Python guarda uma versão compilada do models.py e só a refaz se a data ou o tamanho
    # mudarem; apagando a pasta, o próximo teste lê o arquivo com o bug com certeza.
    shutil.rmtree(MODELS.parent / "__pycache__", ignore_errors=True)
    RESPOSTA.parent.mkdir(parents=True, exist_ok=True)
    RESPOSTA.write_text(json.dumps(bug, ensure_ascii=False, indent=2), encoding="utf-8")
    # O bug vira um commit: assim o git diff da correção mostra exatamente o que você consertou.
    subprocess.run(["git", "commit", "-q", "-m", "chore: bug plantado (desafio M04A)", "--",
                    str(MODELS)], cwd=PASTA_PROJETO, check=True)
    print(f"Bug plantado e commitado (um entre {len(possiveis)} possíveis).")
    print("O jogo continua abrindo; os testes do módulo continuam verdes.")
    print("Agora escreva o teste que o encontra. Travou? python ferramentas/plantar_bug.py --dica")
    return 0


def mostrar(campo):
    if not RESPOSTA.exists():
        print("Nenhum bug plantado.")
        return 1
    bug = json.loads(RESPOSTA.read_text(encoding="utf-8"))
    if campo == "dica":
        print(f"Dica: {bug['dica']}")
        return 0
    print(f"O bug era: {bug['nome']}.")
    print(f"Sintoma: {bug['sintoma']}")
    if re.search(bug["padrao"], MODELS.read_text(encoding="utf-8")):
        RESPOSTA.unlink()  # corrigido: a próxima rodada pode plantar outro
        print("Corrigido no models.py. Confira a correção com: git diff src/models.py")
    else:
        print("A linha original não voltou ao models.py. Se você corrigiu de outro jeito,")
        print("confira com git diff src/models.py e apague ferramentas/saida/bug_plantado.json.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Planta um bug escondido no src/models.py.")
    grupo = parser.add_mutually_exclusive_group()
    grupo.add_argument("--dica", action="store_true", help="uma dica de onde procurar")
    grupo.add_argument("--revelar", action="store_true", help="mostra qual foi o bug")
    args = parser.parse_args()
    if args.dica:
        return mostrar("dica")
    if args.revelar:
        return mostrar("revelar")
    return plantar()


if __name__ == "__main__":
    sys.exit(main())
