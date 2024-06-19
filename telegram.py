import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

telegram_bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

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

def forward_message_to_user(chat_id, message):
    telegram_bot.send_message(chat_id=chat_id, text=message)

def echo_user_message(update, context):
    received_text = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text=received_text)

def handle_error(update, context):
    error_message = f"Update {update} caused error {context.error}"
    print(error_message)

def run_bot():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", greet_user))
    dispatcher.add_handler(CommandHandler("help", display_help))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo_user_messages))

    dispatcher.add_error_handler(handle_error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    run_bot()