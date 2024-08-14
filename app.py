import time

from flask import Flask, request
from threading import Thread
from pyrogram import filters, Client

# Bot and User configuration
api_id = "7769505"
api_hash = "33f551652408cce07cf7e7621560021a"
bot_token = "7457733532:AAEcC_L4eKRagZIs4g5uq5JAhM7d8VXHKVE"
URL = "http://127.0.0.1:5000"
file_base_channel = -1002203067739
file_url_bot = 2138323286
# Initialize bot and user clients
bot = Client('bot',
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token,
             workers=6
             )

user = Client('user_session',
              api_id=api_id,
              api_hash=api_hash,
              workers=6
              )

# Flask app initialization
app = Flask(__name__)


# Define a route for the Flask app
@app.route('/')
def index():
    return "Bot is running!"


@app.route('/send_message/<int:chat_id>/<message>')
def send_message(chat_id, message):
    # Send a message using the bot
    bot.send_message(chat_id, message)
    return f"Message sent to chat_id {chat_id}: {message}"


@app.route('/download')
def download():
    # Capture the file_id from the query parameter
    file_id = request.args.get('file_id')
    change_url = None

    if not file_id:
        return "No file_id provided!", 400
    searched = user.search_messages(file_base_channel, query=f"file_id: {file_id}", limit=1)
    if searched:
        for i in searched:
            user.copy_message(file_url_bot, i.chat.id, i.id)
            time.sleep(1)

        for i in user.search_messages(file_url_bot, query=f"", limit=1):
            message = i
            given_url = message.text
            given_url = given_url[given_url.index("📥 Download: ") + 15:]
            given_url = given_url[:given_url.index("\n")]

            change_url = given_url.replace("https://dl.springsfern.in/","https://api.springsfern.in/")
            change_url = change_url[:change_url.index("?mime=")]

            """https://api.springsfern.in/dl/611736/Locke.and.Key.S01E09.WEBRip-[CineSubz.com]-720p.mp4"""
            """https://dl.springsfern.in/dl/611736/Locke.and.Key.S01E09.WEBRip-%5BCineSubz.com%5D-720p.mp4?mime=video/mp4&size=307392640"""

            time.sleep(1)
        return f"Captured file_id: {change_url}"
    else:
        return "Not file found"


# Bot event handler
@bot.on_message(filters.private & filters.command(['start']))
def welcome(_, message):
    bot.send_message(message.chat.id, "Welcome! The bot is connected to a Flask app.")


# Bot file handler
@bot.on_message(filters.private & filters.document | filters.photo | filters.video | filters.audio)
def document(_, message):
    print(message)
    if message.document:
        pass
    elif message.photo:
        message.document = message.photo
    elif message.video:
        message.document = message.video
    elif message.audio:
        message.document = message.audio

    bot.copy_message(file_base_channel, message.chat.id, message.id,
                     caption="file_id: " + str(message.document.file_unique_id))
    text = URL + f"/download?file_id={message.document.file_unique_id}"
    bot.send_message(message.chat.id, text)


# Function to run Flask in a separate thread
def run_flask():
    app.run(port=5000)


# Run the Flask app in a separate thread
if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Start bot in the main thread and keep it running
    bot.start()
    user.start()

    # Block the main thread with idle to keep bot running
    from pyrogram import idle

    idle()

    # Stop bot and user clients when exiting
    bot.stop()
    user.stop()
