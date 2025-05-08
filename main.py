import random
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler

TOKEN = "7890540111:AAGiYQ3CVlt4owg67-jeKusldFYIc6syAdE"
URL = f"https://cryptocritters.onrender.com/{TOKEN}"

app = Flask(__name__)
bot = Bot(token=TOKEN)

# In-memory user data (can be replaced with a database)
user_data = {}

# List of available critters
critters = [
    {
        "name": "Byteclaw",
        "rarity": "Common",
        "image": "https://i.imgur.com/MDOz7mv.png",
        "description": "A digital crustacean with a sharp sense of mischief."
    },
    {
        "name": "Cryphos",
        "rarity": "Rare",
        "image": "https://i.imgur.com/5lnltnE.png",
        "description": "An elusive spirit of the blockchain realm."
    },
    {
        "name": "Sparkfang",
        "rarity": "Epic",
        "image": "https://i.imgur.com/IJdZJUS.png",
        "description": "A crackling feline made of pure energy."
    },
    {
        "name": "Glitchtail",
        "rarity": "Legendary",
        "image": "https://i.imgur.com/Z9YXaS2.png",
        "description": "A mysterious critter warped by code."
    },
    {
        "name": "Nebuluff",
        "rarity": "Mythic",
        "image": "https://i.imgur.com/XF7mDQK.png",
        "description": "A celestial pup born from the cloud."
    }
]

# Handlers
def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Hatch Egg", callback_data="hatch")],
        [InlineKeyboardButton("Show My Critter", callback_data="show")],
        [InlineKeyboardButton("Train", callback_data="train")],
        [InlineKeyboardButton("Feed", callback_data="feed")],
        [InlineKeyboardButton("Critter Inventory", callback_data="inventory")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome to CryptoCritters! Get ready to hatch your digital pet.", reply_markup=reply_markup)

def handle_button(update: Update, context):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()

    if query.data == "hatch":
        if user_id in user_data:
            query.edit_message_text("You already hatched a critter!")
        else:
            critter = random.choice(critters)
            user_data[user_id] = {"critter": critter, "level": 1}
            msg = f"You hatched a {critter['rarity']} critter: {critter['name']}!\n{critter['description']}\nLevel: 1"
            bot.send_photo(chat_id=user_id, photo=critter["image"], caption=msg)
    elif query.data == "show":
        if user_id not in user_data:
            query.edit_message_text("You haven't hatched a critter yet!")
        else:
            c = user_data[user_id]["critter"]
            lvl = user_data[user_id]["level"]
            msg = f"{c['name']} ({c['rarity']})\n{c['description']}\nLevel: {lvl}"
            bot.send_photo(chat_id=user_id, photo=c["image"], caption=msg)
    elif query.data == "train":
        if user_id not in user_data:
            query.edit_message_text("Hatch a critter first!")
        else:
            user_data[user_id]["level"] += 1
            lvl = user_data[user_id]["level"]
            bot.send_message(chat_id=user_id, text=f"Your critter trained and reached level {lvl}!")
    elif query.data == "feed":
        if user_id not in user_data:
            query.edit_message_text("Hatch a critter first!")
        else:
            bot.send_message(chat_id=user_id, text="*nom nom nom* Your critter enjoyed the snack!")
    elif query.data == "inventory":
        if user_id not in user_data:
            query.edit_message_text("No critters collected yet.")
        else:
            c = user_data[user_id]["critter"]
            bot.send_message(chat_id=user_id, text=f"Inventory:\n1. {c['name']} ({c['rarity']})")

@app.route(f'/{TOKEN}', methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route('/')
def index():
    return "CryptoCritters Bot is running!"

# Setup dispatcher
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(handle_button))

if __name__ == '__main__':
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
