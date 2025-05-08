import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from fluent import sender

TELEGRAM_TOKEN = "8077690095:AAG0R5hErSaeed70YS6rvf8tfSOdDo8VFBQ"

fluent_sender = sender.FluentSender('telegram.bot', host='fluentd', port=24224)

logger = logging.getLogger('telegram_bot')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
в
def log_to_fluent(level: str, extra_data: dict):
    record = {
        'timestamp': datetime.utcnow().isoformat(),
        'level': level,
        **extra_data 
    }
    if fluent_sender:
        if not fluent_sender.emit(level, record):
            logger.warning("Fluentd: emit() failed")
    else:
        logger.warning("Fluentd: Sender is not initialized")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message_text = f"Користувач {user_id} надіслав /start"
    logger.info(message_text)
    log_to_fluent('info', {
        'event': 'bot_start',
        'user_id': user_id,
        'command': '/start',
        'message': message_text
    })
    await update.message.reply_text("Бот працює! 👋")

def main():
    start_msg = "Запуск бота Telegram"
    logger.info(start_msg)
    log_to_fluent('info', {
        'event': 'bot_startup',
        'message': start_msg
    })

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
