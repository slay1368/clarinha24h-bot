
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Token do seu bot
BOT_TOKEN = "8186316328:AAHnv7iaIV78mVLZszjPbvu4eB-nkBMv4a"

# Armazena quantas mensagens cada usuário enviou
user_message_counts = {}

# Mensagens de boas-vindas e respostas programadas
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(clarinha_messages[0])
    user_message_counts[update.effective_user.id] = 1

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    count = user_message_counts.get(user_id, 0)

    if count < len(clarinha_messages):
        await update.message.reply_text(clarinha_messages[count])
        user_message_counts[user_id] = count + 1
    else:
        await update.message.reply_text(final_message)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Clarinha24hBot is running...")
app.run_polling()
