import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import threading
from queue import Queue
from time import sleep

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

telegram_bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

message_queue = Queue()

def greet_user(update, context):
    welcome_message = "Welcome to EVMWalletTracker notifications!"
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

def display_help(update, context):
    help_message = (
        "This bot will send you notifications for your EVM Wallet.\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Get help info"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)

def forward_messages_to_users():
    while True:
        if not message_queue.empty():
            message, chat_id = message_queue.get()
            telegram_bot.send_message(chat_id=chat_id, text=message)
        sleep(10)

def forward_message_to_user(chat_id, message):
    message_queue.put((message, chat_id))

def echo_user_message(update, context):
    received_text = update.message.text
    forward_message_to_user(update.effective_chat.id, received_text)

def handle_error(update, context):
    error_message = f"Update {update} caused error {context.error}"
    print(error_message)

def run_bot():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", greet_user))
    dispatcher.add_handler(CommandHandler("help", display_help))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo_user_message))

    dispatcher.add_error_handler(handle_error)

    threading.Thread(target=forward_messages_to_users, daemon=True).start()

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    run_bot()