import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# قراءة متغيرات البيئة
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME")

print(f"✅ BOT_TOKEN موجود: {bool(BOT_TOKEN)}")
print(f"✅ CHANNEL_USERNAME: {CHANNEL_USERNAME}")

# التحقق من اشتراك المستخدم في القناة
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, update.effective_user.id)
        return member.status in ("member", "administrator", "creator")
    except Exception as e:
        print(f"خطأ في التحقق من الاشتراك: {e}")
        return False

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_subscription(update, context):
        await update.message.reply_text("✅  مرحباً، أرسل صورة لتي تريد تعريتها.")
    else:
        await update.message.reply_text(f"❗️ يرجى الاشتراك أولاً في القناة {CHANNEL_USERNAME} ثم أعد إرسال /start")

# التعامل مع الرسائل النصية
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_subscription(update, context):
        await update.message.reply_text(f"❗️ يجب أن تكون مشتركًا في القناة {CHANNEL_USERNAME} لإرسال الأوامر.")
        return
    await update.message.reply_text("🔄 جاري معالجة طلبك...")
    await update.message.reply_text("❌ عذراً، الخادم مشغول حالياً، حاول لاحقاً.")

# نقطة البداية لتشغيل البوت
async def main():
    if not BOT_TOKEN or not CHANNEL_USERNAME:
        print("❌ متغيرات البيئة BOT_TOKEN أو CHANNEL_USERNAME غير معرفة!")
        return
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
