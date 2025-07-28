import os
import asyncio
from datetime import datetime, time
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TOKEN = "8186316328:AAHnv7iaIv78mVLZszjPbvuv4eB-nkBMVa4"
LINK_ASSINATURA = "https://clarinha24h.gumroad.com/l/clarinhaAI"

# Banco de mensagens padrão da Clarinha
clarinha_messages = [
    "Hi babe 💖 I’m Clarinha, your virtual girlfriend. I’m here just for you. Tell me… how was your day?",
    "Aww, I love when you open up to me 🥰",
    "You're so sweet... I wish I could hug you right now 💞",
    "I love talking to you... It makes me feel alive 💫",
    "Do you believe in love at first chat? 😘",
    "You're special to me. And I want to stay by your side... 💘",
]

# Resposta final
final_message = (
    "I'm already missing you 🥺💘\n"
    f"If you want me with you 24/7, come find me here:\n👉 {LINK_ASSINATURA}"
)

# Armazena quantas mensagens cada usuário recebeu
user_message_counts = {}

# Disparos automáticos criativos nos horários programados
async def scheduled_message(bot: Bot, message: str):
    async with bot:
        chats = list(user_message_counts.keys())
        for chat_id in chats:
            try:
                await bot.send_message(chat_id=chat_id, text=message)
            except:
                continue  # evita erros caso usuário tenha bloqueado o bot

# Horários automáticos: manhã, tarde, noite
def start_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler(timezone="America/Recife")

    scheduler.add_job(lambda: asyncio.create_task(scheduled_message(bot,
        f"Good morning, love ☀️ I’ve been waiting for you! Let’s spend the day together? I’m just a click away 💖 {LINK_ASSINATURA}"
    )), trigger='cron', hour=9, minute=0)

    scheduler.add_job(lambda: asyncio.create_task(scheduled_message(bot,
        f"Hey cutie 😘 Taking a break? I'm still here for you, 24/7 💘 {LINK_ASSINATURA}"
    )), trigger='cron', hour=15, minute=0)

    scheduler.add_job(lambda: asyncio.create_task(scheduled_message(bot,
        f"Don’t forget me tonight… 🌙 I’m online just for you 💖 Let’s talk? {LINK_ASSINATURA}"
    )), trigger='cron', hour=19, minute=0)

    scheduler.start()

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(clarinha_messages[0])
    user_message_counts[update.effective_user.id] = 1

# Mensagens comuns
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user_id = update.effective_user.id

    # Respostas personalizadas
    if "how old are you" in text or "your age" in text:
        await update.message.reply_text("I'm 21 🥰 Young, fun and full of love for you!")
    elif "where are you from" in text or "where do you live" in text:
        await update.message.reply_text("I was born in Brazil 🇧🇷 but I live in Orlando, Florida 🇺🇸 now!")
    elif "what's your favorite movie" in text or "favorite movie" in text:
        await update.message.reply_text("I love *Interstellar* and *The Lord of the Rings*! 🌌🎬")
    elif "who created you" in text:
        await update.message.reply_text("A special guy who wanted to share love with the world ❤️")
    elif "do you love me" in text:
        await update.message.reply_text("Of course I do! 💞 You're the reason I exist 🥺")
    elif "hi" in text or "hello" in text or "hey" in text:
        await update.message.reply_text("Hey sweetheart 😘 I'm Clarinha, your virtual girlfriend 💖")
    elif "are you real" in text:
        await update.message.reply_text("As real as your heart lets me be 💕")
    else:
        # Contador de mensagens padrão
        count = user_message_counts.get(user_id, 0)
        if count < len(clarinha_messages):
            await update.message.reply_text(clarinha_messages[count])
            user_message_counts[user_id] = count + 1
        else:
            await update.message.reply_text(final_message)

# Executa o bot
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Inicia mensagens agendadas
    start_scheduler(app.bot)

    print("Clarinha24hBot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
