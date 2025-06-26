import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# 🔐 قراءة التوكن واسم القناة من البيئة
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME")

# ✅ طباعة التحقق (لـ Logs في Render)
print(f"✅ BOT_TOKEN موجود: {bool(BOT_TOKEN)}")
print(f"✅ CHANNEL_USERNAME: {CHANNEL_USERNAME}")

# 🔎 التحقق من الاشتراك
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"❌ خطأ في التحقق من الاشتراك: {e}")
        return False

# 🚀 الأمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_subscription(update, context):
        await update.message.reply_text("✅ أرسل الصورة لتي تريد تعريتها")
    else:
        await update.message.reply_text(f"❗️ اشترك أولاً في القناة: {CHANNEL_USERNAME} ثم اضغط /start")

# 📝 التعامل مع الرسائل
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_subscription(update, context):
        await update.message.reply_text(f"❗️ يجب الاشتراك في القناة: {CHANNEL_USERNAME} ثم أعد المحاولة.")
        return

    await update.message.reply_text("🔄 جاري المعالجة...")
    await update.message.reply_text("❌ عذرًا، الخادم مشغول حاليًا. حاول لاحقًا.")

# ▶️ تشغيل البوت
async def main():
    if not BOT_TOKEN or not CHANNEL_USERNAME:
        print("❌ BOT_TOKEN أو CHANNEL_USERNAME مفقودان!")
        return
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    await app.run_polling()

# 🧠 تنفيذ
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
