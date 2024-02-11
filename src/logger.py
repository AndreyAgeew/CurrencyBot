import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="app.log",  # Файл, куда будут записываться логи
    filemode="a",
)  # Режим 'a' означает добавление логов в конец файла

# Создание логгера
logger = logging.getLogger(__name__)

# Добавление обработчика для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Добавление обработчика в логгер
logger.addHandler(console_handler)

# Установка уровня логирования
logger.setLevel(logging.INFO)
