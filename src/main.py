from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import TELEGRAM_TOKEN
from src.bot import convert, handle_message, help, start


def main():
    """
    Основная функция, запускающая бота.

    Эта функция создаёт экземпляр приложения бота, регистрирует обработчики для команд /start, /help, /convert,
    а также обработчик для обычных текстовых сообщений. После регистрации обработчиков, функция запускает
    бота в режиме опроса (polling), что позволяет боту постоянно проверять наличие новых сообщений и реагировать
    на них в реальном времени.
    """
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Регистрация обработчика для обработки текстовых сообщений, не являющихся командами
    handle_message_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), handle_message
    )
    # Регистрация обработчиков для команд
    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", help)
    convert_currency_handler = CommandHandler("convert", convert)

    # Добавление зарегистрированных обработчиков в приложение бота
    application.add_handler(handle_message_handler)
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(convert_currency_handler)

    # Запуск бота для опроса серверов Telegram на наличие новых сообщений
    application.run_polling()


if __name__ == "__main__":
    main()
