import os
import logging
import requests
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler, 
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)
load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'ver_tarefas':
        lista = context.user_data.get('tarefas', [])
        if not lista:
            texto = 'Você não tem tarefas pendentes.'
        else:
            texto = 'Suas tarefas:\n' + '\n'.join(f'{i+1}. {t}' for i, t in enumerate(lista))
        await query.edit_message_text(texto)
    elif query.data == 'ver_ajuda':
        await query.edit_message_text(
            'Comandos disponíveis:\n'
            '/start — Mensagem de boas-vindas\n'
            '/ajuda — Mostra esta lista de comandos\n'
            '/tarefa — Registra alguma tarefa\n'
            '/tarefas — Lista todas as suas tarefas registradas\n'
            '/motivacao — Receba uma frase motivacional em inglês\n'
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton('📋 Minhas Tarefas', callback_data='ver_tarefas')],
        [InlineKeyboardButton('❓ Ajuda', callback_data='ver_ajuda')]
    ])
    await update.message.reply_text(
        'Olá eu sou o Focativo 🎯\n'
        'Te ajudo a manter o foco e organizar suas tarefas.\n'
    , reply_markup=teclado)
async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Comandos disponíveis:\n'
        '/start — Mensagem de boas-vindas\n'
        '/ajuda — Mostra esta lista de comandos\n'
        '/tarefa — Registra alguma tarefa\n'
        '/tarefas — Lista todas as suas tarefas registradas\n'
        '/motivacao — Receba uma frase motivacional em inglês\n'
)
MAX_TAREFAS_LEN = 200
async def tarefa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = ' '.join(context.args)
    if not texto:
        await update.message.reply_text('Use assim: /tarefa Lavar a louça')
        return
    if len(texto) > MAX_TAREFAS_LEN:
        await update.message.reply_text(
            f'Essa tarefa está grande demais ({len(texto)} caracteres)! Por favor, tente resumir em até {MAX_TAREFAS_LEN} caracteres.'
        )
        return
    context.user_data.setdefault('tarefas', []).append(texto)
    await update.message.reply_text(f'Tarefa adicionada: {texto}')

async def tarefas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = context.user_data.get('tarefas', [])
    if not lista:
        await update.message.reply_text('Você não tem tarefas pendentes.')
        return
    texto = '\n'.join(f'{i+1}. {t}' for i, t in enumerate(lista))
    try:
        await update.message.reply_text(f'Suas tarefas:\n{texto}')
    except Exception as e:
        logging.error(f'Erro ao enviar lista de tarefas: {e}')
        await update.message.reply_text(
            'Sua lista de tarefas ficou grande demais para eu enviar aqui 😅\n'
        )
async def motivacao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        resposta = requests.get('https://zenquotes.io/api/random', timeout=5)
        dado = resposta.json()[0]
        texto = f'"{dado["q"]}"\n- {dado["a"]} (via zenquotes.io)'
    except Exception as e:
        logging.error(f'Erro ao buscar citação motivacional: {e}')
        texto = 'Não consegui buscar uma frase agora. Tente novamente daqui a pouco!'
    await update.message.reply_text(texto)

async def comando_desconhecido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Desculpe, não conheço esse comando 🤔\nDigite /ajuda para ver os comandos disponíveis.')

respostas = {
    'oi': 'Oi! Pronto para colocar suas tarefas em dia? 🎯',
    'ola': 'Olá! Pronto para colocar suas tarefas em dia? 🎯',
    'olá': 'Olá! Pronto para colocar suas tarefas em dia? 🎯',
    'obrigado': 'De nada! Estou aqui para te ajudar a manter o foco e organizar suas tarefas.',
    'obrigada': 'De nada! Estou aqui para te ajudar a manter o foco e organizar suas tarefas.',
    'pomodoro': 'Em breve vou ter um comando /pomodoro para ajudar a organizar seus pomodoros! ⏱️',
    'tchau': 'Tchau! Até a próxima! 👋'
}

async def responder_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    resposta = respostas.get(texto)

    for palavra, resposta in respostas.items():
        if palavra in texto:
            await update.message.reply_text(resposta)
            return
    await update.message.reply_text(
        'Desculpe, não entendi. Digite /ajuda para ver os comandos disponíveis.'
)
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.error("Erro ao processar atualização:", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            'Ops, algo deu errado aqui do meu lado ☹️\n Tente novamente mais tarde ou digite /ajuda para ver os comandos disponíveis.'
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('ajuda', ajuda))
app.add_handler(CommandHandler('tarefa', tarefa))
app.add_handler(CommandHandler('tarefas', tarefas))
app.add_handler(CommandHandler('motivacao', motivacao))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_texto))
app.add_handler(MessageHandler(filters.COMMAND, comando_desconhecido))
app.add_error_handler(error_handler)
app.run_polling()