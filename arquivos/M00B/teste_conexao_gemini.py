"""
RPG Engine — Módulo 00: teste de conexão com o Gemini.

Valida a chave, o modelo e a cota ANTES de colocarmos IA no jogo.
Uso:  python teste_conexao_gemini.py
"""
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai

PASTA_PROJETO = Path(__file__).resolve().parent
load_dotenv(PASTA_PROJETO / ".env")

CHAVE = os.getenv("GEMINI_API_KEY")
MODELO = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
TIMEOUT_MS = 30_000  # sem isso, uma rede travada deixaria o programa esperando para sempre

# Erros de rede da Interactions API (o SDK não exporta essas classes publicamente).
ERROS_DE_CONEXAO = ("APIConnectionError", "APITimeoutError")


def explicar_erro(erro):
    """Traduz o erro da API numa orientação prática. Devolve None se não for erro da API."""
    codigo = getattr(erro, "status_code", None) or getattr(erro, "code", None)
    if codigo == 429:
        return "Cota esgotada (429). Espere um minuto e tente de novo."
    if codigo in (400, 401, 403):
        return (f"Requisição recusada ({codigo}). Quase sempre é a chave: "
                "confira GEMINI_API_KEY no arquivo .env.")
    if codigo == 404:
        return f"Modelo não encontrado (404). Confira GEMINI_MODEL={MODELO} no .env."
    if codigo:
        return f"A API respondeu com erro {codigo}: {erro}"
    if type(erro).__name__ in ERROS_DE_CONEXAO:
        return f"Sem conexão com a API (rede, proxy ou firewall): {erro}"
    return None  # não é erro da API: provavelmente um erro no nosso código


def main():
    if not CHAVE or CHAVE == "cole_sua_chave_aqui":
        print("[ERRO] GEMINI_API_KEY não configurada.")
        print("Copie .env.example para .env e cole sua chave do Google AI Studio.")
        sys.exit(1)

    cliente = genai.Client(api_key=CHAVE, http_options={"timeout": TIMEOUT_MS})
    print(f"[REDE] Testando o modelo {MODELO}...")
    inicio = time.perf_counter()
    try:
        interacao = cliente.interactions.create(
            model=MODELO,
            system_instruction=(
                "Você é o narrador de um RPG medieval. "
                "Responda em português, em uma única frase curta."
            ),
            input="Dê boas-vindas a um engenheiro júnior que acabou de montar sua bancada.",
            store=False,  # não guarda a interação para continuar a conversa depois
        )
    except Exception as erro:
        mensagem = explicar_erro(erro)
        if mensagem is None:
            raise  # erro de programação: mostra o traceback completo para corrigir
        print(f"[ERRO] {mensagem}")
        sys.exit(1)

    duracao = time.perf_counter() - inicio
    print(f"[OK] Resposta em {duracao:.1f} s:")
    print(interacao.output_text)


if __name__ == "__main__":
    main()
