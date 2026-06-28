import asyncio
import os
import logging
from turn_off.turn_off_led import turn_off_led
from turn_on.turn_on_led import turn_on_led
from red_light_check.red_light_on_check import is_night_light_on

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "sync_night_light.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),  # Залишаємо вивід у консоль для зручності
    ],
)


async def main():
    logging.info("Скрипт повного моніторингу нічного світла запущено...")

    # Фіксуємо стартовий стан системи
    was_on = is_night_light_on()

    while True:
        current_on = is_night_light_on()

        # Тригер А: Нічник щойно увімкнувся (перехід з False у True)
        if current_on and not was_on:
            logging.info("Нічне світло активувалось. Вмикаю LED-стрічку...")
            await turn_on_led()
            logging.info("Команду ввімкнення завершено.")

        # Тригер Б: Нічник щойно вимкнувся (перехід з True у False)
        elif not current_on and was_on:
            logging.info("Нічне світло вимкнулось. Вимикаю LED-стрічку...")
            await turn_off_led()
            logging.info("Команду вимкнення завершено.")

        # Оновлюємо попередній стан для наступної ітерації
        was_on = current_on

        # Перевірка кожні 4 секунди
        await asyncio.sleep(4)


if __name__ == "__main__":
    asyncio.run(main())
