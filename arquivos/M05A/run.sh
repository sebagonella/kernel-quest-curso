#!/usr/bin/env bash
# Roda o jogo no Linux: ./run.sh (de qualquer pasta; argumentos extras vão para o main.py).
set -e  # se um comando falhar, o script para ali (em vez de seguir com o erro)

# A pasta deste script é a raiz do projeto: dali o jogo acha a venv e os assets.
cd "$(dirname "$0")"

# TODO (desafio): sem o arquivo .env, o jogo abre sem a chave e só reclama na primeira fala.
#       Pare aqui com uma mensagem clara (o que falta e o comando que resolve) e exit 1.

# Ativa a venv do projeto: daqui em diante, "python" é o Python dela, com os pacotes do jogo.
source .venv/bin/activate
exec python main.py "$@"  # exec: o jogo ocupa o lugar do script (um processo só no ps)
