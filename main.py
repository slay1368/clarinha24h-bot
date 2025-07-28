from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import threading
import time
import os
from datetime import datetime

# Token do Bot
BOT_TOKEN = os.getenv("BOT_TOKEN", "8186316328:AAHnv7iaIv78mVLZszjPbvuv4eB-nkBMVa4")

# Frases da Clarinha
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

user_message_counts = {}

# Palavras-chave e respostas
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

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    update.message.reply_text(clarinha_messages[0])
    user_message_counts[user_id] = 1

def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = update.message.text.lower().strip()

    for key in custom_replies:
        if key in text:
            update.message.reply_text(custom_replies[key])
            return

    count = user_message_counts.get(user_id, 0)
    if count < len(clarinha_messages):
        update.message.reply_text(clarinha_messages[count])
        user_message_counts[user_id] = count + 1
    else:
        update.message.reply_text(final_message)

def send_scheduled_reminders(bot: Bot):
    while True:
        now = datetime.now()
        hour = now.hour
        msg = None

        if hour == 9:
            msg = "🌞 Good morning, love! Just reminding you that I’m always here... 24/7 for you 💖\n👉 https://clarinha24h.gumroad.com/l/clarinhaAI"
        elif hour == 15:
            msg = "☕ Thinking of you this afternoon... Let’s talk more?\nI’m online anytime, babe 💬💘\n👉 https://clarinha24h.gumroad.com/l/clarinhaAI"
        elif hour == 19:
            msg = "🌆 The evening is perfect to be with someone special... I'm here, just one click away 🥰\n👉 https://clarinha24h.gumroad.com/l/clarinhaAI"

        if msg:
            for user_id in user_message_counts:
                try:
                    bot.send_message(chat_id=user_id, text=msg)
                except Exception as e:
                    print(f"Erro ao enviar para {user_id}: {e}")
        
        time.sleep(3600)  # Verifica a cada 1h

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    threading.Thread(target=send_scheduled_reminders, args=(updater.bot,), daemon=True).start()

    print("Clarinha24hBot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
