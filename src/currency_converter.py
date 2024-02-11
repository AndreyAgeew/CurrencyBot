from decimal import Decimal

import requests

from config import CURRENCY_API_URL


def convert_currency(amount: Decimal, from_currency: str, to_currency: str) -> Decimal:
    """
    Конвертирует заданную сумму из одной валюты в другую, используя внешний API для получения курсов валют.

    Делает HTTP-запрос к внешнему API курсов валют, извлекает курс обмена для целевой валюты и возвращает
    результат конвертации исходной суммы в целевую валюту в формате Decimal для повышенной точности.
    Возвращает None, если конвертация невозможна из-за ошибки запроса или отсутствия курса обмена.

    Параметры:
        amount (Decimal): Сумма для конвертации.
        from_currency (str): Код исходной валюты (например, "USD").
        to_currency (str): Код целевой валюты (например, "EUR").

    Возвращает:
        Decimal: Конвертированная сумма в целевой валюте. Возвращает None, если конвертация не удалась.

    Примеры использования:
        convert_currency(Decimal('100.00'), 'USD', 'EUR')
        Decimal('88.50')  # Предполагается, что курс 1 USD = 0.885 EUR
    """
    response = requests.get(f"{CURRENCY_API_URL}{from_currency}")
    if response.status_code == 200:
        rates = response.json().get("rates")
        to_rate = rates.get(to_currency)
        if to_rate:
            converted_amount = amount * Decimal(str(to_rate))
            return converted_amount.quantize(
                Decimal("0.01")
            )  # Округление до центов/копеек
    return None
