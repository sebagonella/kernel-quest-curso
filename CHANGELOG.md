# Changelog

O que mudou em cada versão do material. Correções de uma parte que você já fez aparecem aqui: confira antes de seguir para a próxima.

## v0.11.0

**O que fazer:** traga a pasta nova (`git -C ~/kernel-quest-curso pull` e `cp -r ~/kernel-quest-curso/arquivos/M06B ~/curso-arquivos/`) e abra o M06B. O módulo instala uma dependência nova (`pip install -r requirements.txt`, no Passo 1).

- M06B — IA que age: a resposta da IA vira dados validados (saída estruturada com Pydantic: fala, emoção e ação), balões de emoção acima dos NPCs, o painel "Receber" da Chave da Masmorra depois da missão do Mago, a loja do Brok aberta pela conversa, o Guarda do Portão e a função que decide o que a IA pode fazer no jogo (defesa contra injeção de prompt).

## v0.10.0

**O que fazer:** traga a pasta nova (`git -C ~/kernel-quest-curso pull` e `cp -r ~/kernel-quest-curso/arquivos/M06A ~/curso-arquivos/`) e abra o M06A.

- M06A — Conversa de verdade: o campo "Sua vez" na conversa (entrada de texto com acento), o NPC que lembra o que foi dito na mesma conversa (Interactions API com `previous_interaction_id`), os tokens gastos no F3, o limite de turnos e a despedida de cada NPC.

## v0.9.1

Correção. **O que fazer:** se você já passou do M00B e ainda não clonou o curso, siga o Passo 8 do M00B agora (o clone em `kernel-quest-curso/`, na sua pasta pessoal) e use daí em diante a linha "Arquivos do curso" do Ponto de partida de cada módulo. Se ainda está no M00A ou no M00B, siga os módulos como estão. Se está entre o M02A e o M03A com a `escrever` antiga (sem o `centro_x`), troque-a pela do Passo 1a do M02A; do M03B em diante ela já vem pronta.

- README: nova seção "Seus repositórios e pastas", com os três repositórios do curso (qual você só lê e em qual você escreve), as pastas na sua pasta pessoal e como os arquivos chegam e se atualizam.
- M00A: novo Passo 0, que baixa os arquivos do curso (ZIP) e cria a pasta `curso-arquivos/`; os prints de entrega ficam em `entregas/`, dentro do projeto.
- M00B: o primeiro commit leva o trabalho do M00A; o `git push` explicado; novo Passo 8, o clone do curso e o mapa dos repositórios; caminho "Sem mentor?" para o `.env` na lista do `git status`; o roteiro de "o `.env` apareceu no GitHub" refeito (apagar a chave antiga, `git rm -r --cached .` e `git add .`, sem recriar o repositório, que enviaria o mesmo histórico de novo); a Issue no seu repositório.
- M01 a M04B: linha "Arquivos do curso" no Ponto de partida (`git pull` do clone e cópia da pasta do módulo). M01 a M02C: prints de entrega dentro do projeto.
- M02A: a `escrever` ganha o parâmetro `centro_x` no Passo 1a (antes, quem resolveu o desafio do M01 de outro jeito recebia um `TypeError` no Passo 2).
- M02C: o Tiled no Linux pelo snap, que já vem no Ubuntu.
- M03C: quem entra pelo repositório-modelo traz os arquivos do curso e convida o mentor; a branch tem seis commits, não cinco.
- M04A: um bloco de código mal fechado no Passo 1 escondia as perguntas e a primeira edição; menus do Tiled em português.
- M04B: placar de testes relativo (o seu número depende dos testes que você escreveu no M04A); o selo do CI antes do merge.
- M05A: quem já fazia o curso no Linux pula os clones; o VS Code no Linux e no WSL2; permissões como o Ubuntu mostra (664/775); `--exclude-dir` no `grep`; `ps aux | grep main.py`.
- M05B: espaços reservados `NUMERO` e `URL_SSH` no lugar de `???`, que o bash expandia.
- M05C: âncora sem o nome de NPC da referência.

## v0.9.0

- M05C — Portas abertas: um servidor SSH na sua máquina, endurecido (só chave, sem root, lista de usuários), uma noite de ataques lida no log e o Quadro da Vigia no jogo; a exposição real fica na Missão no mundo real (opcional).

## v0.8.0

- M05B — Chave SSH e o Tux: o Tux desenhado por você no Piskel, a licença da arte nos créditos e o repositório acessado por chave SSH.

## v0.7.0

- M05A — Território Pinguim: o jogo no Linux (dual boot, WSL2 ou máquina virtual), o ermitão Tux, o sistema e o kernel no HUD, o `run.sh` e o terminal (arquivos, permissões e processos).

## v0.6.0

- M04B — CI e slimes: os testes rodando no GitHub Actions a cada push, slimes na floresta, vida, dano e invencibilidade.

## v0.5.1

- README: nova seção "Começar no meio do curso", com o repositório-modelo (entrada no M03C).
- M03C: orientação para quem chega pelo repositório-modelo.

## v0.5.0

- M04A — Testes: o modo depuração (F3), o baú da floresta e os testes automáticos com pytest.

## v0.4.0

Primeira publicação: módulos M00A a M03C (Fundamentos e início de Engenharia).

- M00A — Primeira janela
- M00B — Chave e Git
- M01 — O Mago responde
- M02A — Mundo vivo
- M02B — Interface
- M02C — Mapas de verdade
- M03A — Moedas e HUD
- M03B — Camadas
- M03C — Loja do Brok e GitHub
