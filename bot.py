import os
import logging
from warnings import filters
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def eco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, eco))

app.run_polling()