# Focativo Bot 🎯

Bot de produtividade para Telegram: gerencia tarefas e ajuda a manter o foco, respondendo automaticamente a comando e mensagens de texto.

## Comandos disponíveis

- `/start` — MENSAGEM DE BOAS-VINDAS
- `/ajuda` — LISTA DE COMANDOS DISPONÍVEIS
- `/tarefa <descrição>` —  ADICIONA UMA TAREFA (ex: `/tarefa Estudar Python`)
- `/tarefas` — LISTA AS TAREFAS PENDENTES

## Tecnologias
- Python 3.10+
- python-telegram-bot
- python-dotenv

## Como rodar localmente

1. Clone o repositório: `git clone https://github.com/thiagoferlopes/focativo-bot.git`
2.  Crie e ative um ambiente virtual, depois instale as dependências: `pip install -r requirements.txt`
3. Crie um arquivo `.env` na raiz com `TELEGRAM_TOKEN=seu_token...`
4. Rode pyhton3 bot.py

## Decisões do projeto
- Validação de tamanho máximo por tarefa, para evitar estourar o limite de caracteres do telegram.
- Handler de erro global, garantindo que o usuário sempre receba um retorno se algo falhar internamente