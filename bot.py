import os
import uuid
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

TOKEN = "8785479296:AAEimxWJYApmL2a54UhXynxaB8QEsWfXYQM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = "أهلاً وسهلاً بيك. نورت، تأمرني بشي؟"
    await update.message.reply_text(welcome_text)

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if not url.startswith("http"):
        return

    msg = await update.message.reply_text("🚀 الك/چ...")

    file_id = str(uuid.uuid4())[:8]
    output_filename = f"video_{file_id}.mp4"

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": output_filename,
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if os.path.exists(output_filename):
            with open(output_filename, "rb") as video:
                await update.message.reply_video(video, caption="عيوني ⚡")
            
            os.remove(output_filename)
            await msg.delete()
        else:
            await msg.edit_text("❌ ماكو هيچ فيديو.")

    except Exception:
        if os.path.exists(output_filename):
            os.remove(output_filename)
        await msg.edit_text("❌ الرابط مايشتغل.")

app = (
    Application.builder()
    .token(TOKEN)
    .read_timeout(60)
    .write_timeout(60)
    .connect_timeout(60)
    .build()
)

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

if __name__ == "__main__":
    print("⚡ Super Fast Bot running...")
    app.run_polling(drop_pending_updates=True)
