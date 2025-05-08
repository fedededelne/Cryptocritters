from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = 7890540111:AAGiYQ3CVlt4owg67-jeKusldFYIc6syAdE
bot = Bot(token=TOKEN)
app = Flask(__name__)

# Inizializza l'app Telegram
telegram_app = Application.builder().token(TOKEN).build()

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to CryptoCritters! Get ready to hatch your digital pet.")

telegram_app.add_handler(CommandHandler("start", start))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    telegram_app.update_queue.put_nowait(update)
    return "OK"

@app.route("/", methods=["GET"])
def index():
    return "CryptoCritters bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
