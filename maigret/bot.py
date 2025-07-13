import os
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Get the token from environment variable
TOKEN = os.getenv("BOT_TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 Welcome to Sniff Maigret Bot!\n"
        "Use this format to search:\n"
        "`/run +919876543210`",
        parse_mode='Markdown'
    )

def run_maigret(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("⚠️ Please provide a phone number. Example:\n`/run +919876543210`", parse_mode='Markdown')
        return

    target = context.args[0]
    update.message.reply_text(f"🔍 Searching for `{target}` using Maigret...", parse_mode='Markdown')

    try:
        # Run maigret command
        result = subprocess.run(
            ['python3', 'maigret.py', target, '--print-found'],
            capture_output=True,
            text=True,
            timeout=90
        )
        output = result.stdout.strip()

        if not output:
            update.message.reply_text("❌ No results found.")
        elif len(output) > 4000:
            update.message.reply_text("📄 Result is too long. Showing first 4000 characters:")
            update.message.reply_text(output[:4000])
        else:
            update.message.reply_text(f"🕵️ Found:\n\n{output}")
    except Exception as e:
        update.message.reply_text(f"🚨 Error occurred:\n{str(e)}")

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("run", run_maigret))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
