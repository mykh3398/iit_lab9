import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from fluent import sender, event

TELEGRAM_TOKEN = "8077690095:AAG0R5hErSaeed70YS6rvf8tfSOdDo8VFBQ"  # 🔒 Замінити на свій токен

# Налаштування Fluentd
fluent_sender = sender.FluentSender('telegram.bot', host='fluentd', port=24224)

# Налаштування стандартного логування
logger = logging.getLogger('telegram_bot')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Функція логування у Fluentd
def log_to_fluent(level: str, message: str):
    try:
        event.Event(level, {'message': message})
    except Exception as e:
        logger.warning(f"Не вдалося відправити лог у Fluentd: {e}")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = f"Користувач {user_id} надіслав /start"
    logger.info(text)
    log_to_fluent('info', text)
    await update.message.reply_text("Бот працює! 👋")

def main():
    start_msg = "Запуск бота Telegram"
    logger.info(start_msg)
    log_to_fluent('info', start_msg)

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
