import os
import sys

from _decimal import Decimal
from telegram import Update
from telegram.ext import (
    CallbackContext,
    ContextTypes,

)

from .currency_converter import convert_currency
from .logger import logger

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Отправляет приветственное сообщение и базовую информацию о боте пользователю.

    Эта команда активируется при первом взаимодействии пользователя с ботом или когда пользователь
    явно вызывает команду /start. Приветственное сообщение содержит краткое описание функционала бота,
    примеры команд и инструкции по их использованию.
    """
    logger.info("Команда /start получена")
    welcome_message = """
                Привет! Я - Ваш Финансовый Помощник Бот 🤖
                
                Я могу помочь вам с конвертацией валют в реальном времени. Вот что я умею:
                
                Если у вас возникнут вопросы, используйте команду /help.
                
                Начните с команды, которая вас интересует, и я постараюсь помочь! 🚀
                """
    await update.message.reply_text(welcome_message)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Отправляет пользователю список доступных команд и инструкции по их использованию.

    Эта команда предназначена для помощи пользователям в понимании функционала бота, предоставляя
    подробные описания каждой доступной команды и примеры их использования. Команда /help может быть
    полезна для новых пользователей или в случаях, когда необходимо быстро вспомнить, как воспользоваться
    определённой функцией бота.
    """
    logger.info("Команда /help получена")
    help_message = """
            Вот список команд, которые я поддерживаю:
            
            /start - Показать приветственное сообщение и базовую информацию о боте.
            /help - Показать этот список команд.
            /convert <сумма> <из валюты> to <в валюту> - Конвертировать сумму из одной валюты в другую.
            
            Примеры использования команд:
            /convert 100 USD to EUR - Конвертирует 100 долларов США в евро.
            
            Если вам нужна дополнительная помощь или у вас есть вопросы о том, как использовать определённые функции, пожалуйста, не стесняйтесь обращаться за помощью.
            
                """
    await update.message.reply_text(help_message)


async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает команду /convert для конвертации суммы из одной валюты в другую.

    Пользователи могут использовать эту команду для запроса конвертации валют по текущему курсу.
    Команда требует указания суммы и пары валют в формате: /convert <сумма> <из валюты> to <в валюту>.
    В случае успеха, бот отправляет сообщение с результатом конвертации. Если произошла ошибка (например,
    неверный формат команды или проблемы с получением курса валют), пользователь получает соответствующее
    уведомление.
    """
    logger.info("Команда /convert получена")
    args = context.args
    if len(args) != 4 or args[2].lower() != "to":
        await update.message.reply_text(
            "Используйте формат: /convert <сумма> <из валюты> to <в валюту>."
        )
        return

    try:
        amount = Decimal(args[0])
        from_currency = args[1].upper()
        to_currency = args[3].upper()
        result = convert_currency(amount, from_currency, to_currency)
        if result is not None:
            await update.message.reply_text(
                f"{amount} {from_currency} = {result} {to_currency}"
            )
        else:
            await update.message.reply_text("Не удалось получить курс валют.")
    except ValueError as e:
        logger.info(f"Ошибка при команде /convert: {e}")
        await update.message.reply_text("Пожалуйста, укажите корректную сумму.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает текстовые сообщения от пользователей.

    Эта функция реагирует на определённые ключевые слова в тексте сообщений. Если сообщение содержит
    слово "привет", функция отвечает приветствием. Если сообщение содержит "пока", функция прощается.
    Во всех остальных случаях функция предлагает использовать команду /help для получения списка доступных команд.
    """
    logger.info("Входящее сообщение обработано")
    text = update.message.text.lower()
    if "привет" in text:
        await update.message.reply_text("Привет!")
    elif "пока" in text:
        await update.message.reply_text("До свидания!")
    else:
        await update.message.reply_text(
            "Не уверен, как на это ответить. Используй /help."
        )


def error(update: Update, context: CallbackContext) -> None:
    """
    Логирует ошибки, вызванные во время обновлений.

    Эта функция предназначена для логирования исключений и ошибок, которые возникают во время обработки
    обновлений от Telegram. Она помогает в отладке, предоставляя подробную информацию об ошибке.
    """
    logger.warning(f'Update "{update}" caused error "{context.error}"')
