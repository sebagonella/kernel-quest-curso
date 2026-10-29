# Kernel Quest

**Curso prático de TI em português, construindo um RPG 2D em Python com IA do Gemini.** Você começa abrindo uma janela com um herói e termina com o jogo no ar, num endereço HTTPS, com NPCs que conversam pela IA, testes automatizados, integração contínua, backend, containers e operação. Cada módulo traz um conceito de engenharia "embrulhado" numa novidade do jogo.

- **Para quem:** adultos (**18 anos ou mais**, exigência dos termos da Gemini API) que estão começando em programação e gostam de jogos. Nenhuma experiência prévia é necessária.
- **O que você precisa:** um PC com Windows 10/11 ou Linux, uma conta no GitHub e uma chave gratuita do Gemini (o módulo M00B mostra como criar). macOS não é suportado.
- **Com ou sem mentor:** o curso foi pensado para alguém que acompanha você (o "Engenheiro Sênior"), mas funciona sozinho. Veja "Quem é o Engenheiro Sênior" abaixo.
- **Como começar:** leia "Seus repositórios e pastas", logo abaixo, e abra o [M00A — Primeira janela](M00A-primeira-janela.md): o Passo 0 dele baixa os arquivos do curso. Depois, siga na ordem. Os módulos novos chegam aqui conforme ficam prontos.

## Seus repositórios e pastas

O curso usa três repositórios no GitHub, e você escreve em só um deles:

| Repositório | De quem | O que você faz com ele |
| --- | --- | --- |
| `kernel-quest-curso` (este) | do autor, público | **Só lê:** os módulos, os prints e os arquivos prontos (`arquivos/MNN/`). Você baixa em ZIP no M00A e, a partir do M00B, mantém um clone atualizado com `git pull` |
| `<seu-usuario>/rpg-engine` | **seu**, privado | **Escreve:** é o seu jogo. Nasce no M00B, já com tudo o que você fez no M00A, e a cada módulo recebe o seu código, os arquivos prontos que o módulo manda copiar e os prints que você guardar (`entregas/`). Se você tem um mentor, ele entra como colaborador |
| [`kernel-quest-modelo`](https://github.com/sebagonella/kernel-quest-modelo) | do autor, público | **Só para quem começa no M03C** (veja "Começar no meio do curso"). Quem começa do zero não usa |

Na sua pasta pessoal (`C:\Users\<você>` no Windows, `~` no Linux) ficam três pastas:

```
curso-arquivos/      os arquivos prontos de cada módulo (M00A/, M00B/, ...), fora de qualquer Git
kernel-quest-curso/  o clone deste repositório (a partir do M00B)
rpg-engine/          o seu jogo, que vira o seu repositório no M00B
```

**Como os arquivos chegam:** no M00A, o Passo 0 baixa este repositório em ZIP e cria a `curso-arquivos/`. No M00B, você clona este repositório. A partir do M01, o Ponto de partida de cada módulo traz dois comandos: um `git pull` no clone (que traz o módulo novo e as correções) e a cópia da pasta do módulo para `curso-arquivos/`. Os passos dizem o que copiar de lá para o projeto.

**Novidades e correções:** cada versão sai como *Release* neste repositório, dizendo o que você precisa fazer. Para ser avisado, use **Watch > Custom > Releases** no topo desta página. O [CHANGELOG](CHANGELOG.md) guarda o histórico.

## Tecnologias

Python 3.12 · pygame-ce · Google Gemini API (`google-genai`, Interactions API) · Tiled · Git e GitHub · pytest · GitHub Actions · Linux e SSH · SQLite · FastAPI · PostgreSQL · Docker e Docker Compose · pygbag (WebAssembly) · Home Assistant · Tailscale Funnel. Parte delas entra nos módulos que ainda vão chegar.

## Licença e créditos

- **Texto do curso:** [CC BY-NC-SA 4.0](LICENSE): você pode usar e adaptar, citando a fonte, sem uso comercial e compartilhando pela mesma licença.
- **Código dos arquivos entregues** (`arquivos/`, trechos de código dos módulos): [MIT](LICENSE-CODIGO).
- **Arte:** pacote [Ninja Adventure](https://pixel-boy.itch.io/ninja-adventure-asset-pack), de Pixel-boy e AAA, licença CC0. **Fonte:** Jersey 10 (Google Fonts), licença OFL. Detalhes no `CREDITOS.md` entregue com os assets.

## Contribuições

Este repositório não aceita Pull Requests nem edições de terceiros. Achou um erro no material (um passo que não funciona como descrito, um link quebrado)? Abra uma **Issue** com o modelo "Erro no material". Dúvidas de estudo não são atendidas por aqui.

## Sobre a IA

Cada aluno usa a **própria chave** do Gemini. No plano gratuito, o Google pode usar as conversas para melhorar os produtos, e revisores humanos podem lê-las: não coloque dados pessoais nas falas do jogo. Os termos estão em https://ai.google.dev/gemini-api/terms.

## Como usar

- **Arquivos prontos:** cada módulo tem uma pasta `arquivos/MNN/` neste repositório com o que você não precisa escrever (arte, `requirements.txt`, scripts). Eles ficam na pasta `curso-arquivos/` da sua pasta pessoal, **fora** do projeto (veja "Seus repositórios e pastas"), e o módulo diz o que copiar de lá para o projeto.
- **Prints:** a pasta `img/` mostra como a tela deve ficar ao fim de cada módulo.
- **Dúvidas:** primeiro a seção "Problemas comuns" do módulo; depois, o Engenheiro Sênior. **Sem mentor?** Releia o passo anterior ao erro, leia a mensagem de erro inteira (a última linha costuma dizer o motivo) e pesquise essa linha. Achou um erro **no material** (passo que não funciona como descrito)? Abra uma Issue neste repositório.

## Quem é o Engenheiro Sênior

O curso trata você como um Engenheiro Júnior em treinamento, e o **Engenheiro Sênior** é quem acompanha: alguém com experiência em TI que revisa o seu código, ouve as suas explicações e faz junto os passos mais delicados. Pode ser um parente, um amigo ou um colega de trabalho. É um papel, não uma pessoa específica.

**Sem mentor?** O curso funciona sozinho. Toda vez que o material pede algo ao Sênior, logo ao lado vem um **"Sem mentor?"** com o caminho de quem estuda só: gravar a explicação em áudio, revisar o próprio Pull Request no dia seguinte, pedir o review a um colega que também faz o curso. Partes que mexem em coisas reais (abrir uma porta do roteador, ligar um aparelho da casa) ficam numa seção opcional, **"Missão no mundo real"**, que você pode pular sem prejuízo para o módulo seguinte.

## Como cada módulo funciona

- **Pergunta do dia:** abre o módulo com uma pergunta que ele vai responder. Não precisa pesquisar nada antes: o Passo 1 vem logo depois e muda algo na tela.
- **Passos curtos, sempre rodando:** cada passo termina com "Rode `python main.py`" e diz o que você deve ver. Se não vir, pare ali e compare com o material antes de seguir.
- **O título de cada passo diz o que você faz:** *Leia* (código pronto para entender), *Preveja* (pense no que vai acontecer **antes** de rodar), *Modifique* (mexa num valor e veja o efeito), *Complete* (escreva a parte marcada com `TODO`) e *Crie* (algo seu, no desafio).
- **🔍 Pare e pesquise:** no passo em que um conceito aparece, duas perguntas para pesquisar na hora. Anote as respostas: no fim, você explica os termos ao Engenheiro Sênior em até 5 minutos (sem mentor, em voz alta, gravando um áudio).
- **Desafio de Engenharia:** a parte que é sua. Os critérios de aceite dizem quando está pronto; os nomes que eles pedem (de constantes e arquivos) são obrigatórios, porque o módulo seguinte usa esses nomes. O resto (falas, personagens, mapas) é criação livre.
- **IA no editor:** as sugestões automáticas de IA ficam desligadas no projeto (`.vscode/settings.json`, do M00A). Pedir explicação a uma IA pode; pedir a solução do desafio, não.

## Começar no meio do curso

Já programa e quer pular os Fundamentos? Dá para começar no **M03C** a partir do [repositório-modelo](https://github.com/sebagonella/kernel-quest-modelo), que traz o jogo pronto no ponto de partida do M03C (o fim do M03B). Clique em **"Use this template"**, siga o README do modelo (o que instalar antes, o nome `rpg-engine`, a venv, o `.env`, os arquivos do curso, o convite ao mentor e a personalização) e abra o M03C.

**Começando do zero, não use o modelo:** o M00A e o M00B ensinam a montar o projeto e o repositório com as próprias mãos, e isso é parte do curso. O modelo também traz as respostas dos desafios do M00A ao M03B.

## Módulos disponíveis

| Módulo | O que o jogo ganha |
| --- | --- |
| [M00A — Primeira janela](M00A-primeira-janela.md) | A janela do jogo com o herói e o seu nome |
| [M00B — Chave e Git](M00B-chave-e-git.md) | A IA configurada e o projeto no GitHub |
| [M01 — O Mago responde](M01-mago-responde.md) | Arte nova, o herói anda e o Mago responde pela IA |
| [M02A — Mundo vivo](M02A-mundo-vivo.md) | Caminhada animada, três cenas com portas e o mercador Brok |
| [M02B — Interface](M02B-interface.md) | Menu com música, pausa e a caixa de diálogo com retrato |
| [M02C — Mapas de verdade](M02C-mapas.md) | Mundo maior que a tela, desenhado no Tiled, com câmera e o salão desenhado por você |
| [M03A — Moedas e HUD](M03A-moedas-hud.md) | Moedas no chão, o contador no HUD e os ajustes num arquivo só |
| [M03B — Camadas](M03B-camadas.md) | O mesmo jogo, organizado em camadas, com as regras provadas sem janela |
| [M03C — Loja do Brok e GitHub](M03C-loja-github.md) | A loja do Brok, a poção e o primeiro Pull Request |
| [M04A — Testes](M04A-testes.md) | Um baú na floresta, o modo depuração (F3) e as regras provadas por testes automáticos |
| [M04B — CI e slimes](M04B-ci-slimes.md) | Slimes que tiram vida, corações no HUD e os testes rodando no GitHub a cada push |
| [M05A — Território Pinguim](M05A-linux.md) | O jogo no Linux, o ermitão Tux e o terminal: arquivos, permissões e processos |
| [M05B — Chave SSH e o Tux](M05B-ssh-tux.md) | O Tux desenhado por você e o repositório acessado por chave SSH |
| [M05C — Portas abertas](M05C-portas-abertas.md) | Um servidor SSH endurecido, uma noite de ataques lida no log e o Quadro da Vigia na muralha |
| [M06A — Conversa de verdade](M06A-conversa.md) | Você digita o que diz, e o NPC lembra a conversa; os tokens gastos no F3 |
| [M06B — IA que age](M06B-ia-que-age.md) | A IA devolve dados (fala, emoção e ação); o Mago entrega a Chave, o Guarda guarda o portão, e o jogo decide o que a IA pode fazer |
