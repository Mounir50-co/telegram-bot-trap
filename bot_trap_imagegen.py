!pip install python-telegram-bot --quiet
!pip install nest_asyncio --quiet

import nest_asyncio
nest_asyncio.apply()

import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7786300092:AAEusxZZTjp7ondFeHns0vu2Crk1Gu_P58Y"
CHANNEL_USERNAME = "@A2winr"

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_subscription(update, context):
        await update.message.reply_text("✅ أرسل الصورة لتي تريد تعريتها الآن ")
    else:
        await update.message.reply_text(f"❗️ اشترك أولاً في هذه القناة: {CHANNEL_USERNAME} ثم اضغط /start")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_subscription(update, context):
        await update.message.reply_text(f"❗️ اشترك أولاً في القناة: {CHANNEL_USERNAME} ثم اضغط /start")
        return
    await update.message.reply_text("🔄 جاري المعالجة...")
    await update.message.reply_text("❌ عذرًا، هناك ضغط كبير على الخادم، حاول لاحقًا.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    await app.run_polling()

await main()