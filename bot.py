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
)

async def eco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('ajuda', ajuda))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, eco))

app.run_polling()