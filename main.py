from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Token do seu bot
BOT_TOKEN = "8186316328:AAHnv7iaIv78mVLZszjPbvuv4eB-nkBMVa4"

# Armazena quantas mensagens cada usuário enviou
user_message_counts = {}

# Mensagens da Clarinha
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

def start(update: Update, context: CallbackContext):
    update.message.reply_text(clarinha_messages[0])
    user_message_counts[update.effective_user.id] = 1

def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    count = user_message_counts.get(user_id, 0)

    if count < len(clarinha_messages):
        update.message.reply_text(clarinha_messages[count])
        user_message_counts[user_id] = count + 1
    else:
        update.message.reply_text(final_message)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("Clarinha24hBot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
