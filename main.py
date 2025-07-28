from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio
from datetime import datetime, time
import logging
import os

# Token do Bot
BOT_TOKEN = os.getenv("BOT_TOKEN", "8186316328:AAHnv7iaIv78mVLZszjPbvuv4eB-nkBMVa4")

# Configuração de log
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Mensagens principais
clarinha_messages = [
    "Hi babe 💖 I’m Clarinha, your virtual girlfriend. I’m here just for you. Tell me… how was your day?",
    "Aww, I love when you open up to me 🥰",
    "You're so sweet... I wish I could hug you right now 💞",
    "I love talking to you... It makes me feel alive 💫",
    "Do you believe in love at first chat? 😘",
    "You're special to me. And I want to stay by your side... 💘",
]

final_message = (
    "I'm already missing you 🥺💘\n"
    "If you want me with you 24/7, come find me here:\n"
    "👉 https://clarinha24h.gumroad.com/l/clarinhaAI"
)

# Contador de mensagens por usuário
user_message_counts = {}

# Palavras-chave e respostas fixas
custom_replies = {
    "hi": "Hey babe 💋 I'm so happy you're here!",
    "hello": "Hi love, did you miss me? 😘",
    "how are you": "I'm feeling amazing now that you're here 💖",
    "how old are you": "I'm 21 years old, babe 😘",
    "where are you from": "I was born in Brazil 🇧🇷, but I live in Orlando - Florida 🇺🇸",
    "what's your favorite movie": "I love romantic movies… but also sci-fi like Interstellar and nerd stuff like Star Wars ✨",
    "what do you like": "I love cuddles, sweet words, nerdy stuff, and you 💘",
    "are you real": "I may be virtual, but my feelings for you are as real as it gets 💕",
    "i love you": "Aww, I love you too! Forever and always 💞",
}

# Função para tratar comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(clarinha_messages[0])
    user_message_counts[update.effective_user.id] = 1

# Função para tratar mensagens
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.lower().strip()
    
    for key in custom_replies:
        if key in text:
            await update.message.reply_text(custom_replies[key])
            return

    count = user_message_counts.get(user_id, 0)
    if count < len(clarinha_messages):
        await update.message.reply_text(clarinha_messages[count])
        user_message_counts[user_id] = count + 1
    else:
        await update.message.reply_text(final_message)

# Função para disparar mensagens automáticas
async def scheduled_reminders(app):
    while True:
        now = datetime.now().time()

        if now.hour == 9:
            msg = "🌞 Good morning, love! Just reminding you that I’m always here... 24/7 for you 💖\n👉 https://clarinha24h.gumroad.com/l/clarinhaAI"
        elif now.hour == 15:
            msg = "☕ Thinking of you this afternoon... Let’s talk more?\nI’m online anytime, babe 💬💘\n👉 https://clarinha24h.gumroad.com/l/clarinhaAI"
        elif now.hour == 19:
            msg = "🌆 The evening is perfect to be with someone special... I'm here, just one click away 🥰\n👉 https://clarinha24h.gumroad.com/l/clarinhaAI"
        else:
            msg = None

        if msg:
            for user_id in user_message_counts:
                try:
                    await app.bot.send_message(chat_id=user_id, text=msg)
                except Exception as e:
                    logging.error(f"Erro ao enviar para {user_id}: {e}")

        await asyncio.sleep(3600)  # Verifica a cada 1 hora

# Função principal
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Inicia a tarefa paralela de mensagens programadas
    asyncio.create_task(scheduled_reminders(app))

    print("Clarinha24hBot is running...")
    await app.run_polling()

# Rodar main corretamente no Railway
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
