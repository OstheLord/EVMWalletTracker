import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to EVMWalletTracker notifications!")

def help_command(update, context):
    help_text = "This bot will send you notifications for your EVM Wallet.\nCommands:\n/start - Start the bot\n/help - Get help info"
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

def send_notification(chat_id, message):
    bot.send_message(chat_id=chat_id, text=message)

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()