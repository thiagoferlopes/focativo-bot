import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler, 
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Olá eu sou o Focativo 🎯\n'
        'Te ajudo a manter o foco e organizar suas tarefas.\n'
        'Digite /ajuda para você ver o que eu sei fazer!'
)
async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Comandos disponíveis:\n'
        '/start — Mensagem de boas-vindas\n'
        '/ajuda — Mostra esta lista de comandos\n'
        '/tarefa — Registra alguma tarefa\n'
        '/tarefas — Lista todas as suas tarefas registradas\n'
)
async def tarefa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = ' '.join(context.args)
    if not texto:
        await update.message.reply_text('Use assim: /tarefa Lavar a louça')
        return
    context.user_data.setdefault('tarefas', []).append(texto)
    await update.message.reply_text(f'Tarefa adicionada: {texto}')

async def tarefas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = context.user_data.get('tarefas', [])
    if not lista:
        await update.message.reply_text('Você não tem tarefas pendentes.')
        return
    texto = '\n'.join(f'{i+1}. {t}' for i, t in enumerate(lista))
    await update.message.reply_text(f'Suas tarefas:\n{texto}')

async def eco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('ajuda', ajuda))
app.add_handler(CommandHandler('tarefa', tarefa))
app.add_handler(CommandHandler('tarefas', tarefas))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, eco))

app.run_polling()