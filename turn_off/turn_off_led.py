import asyncio
import logging
import os
from bleak import BleakClient
from dotenv import load_dotenv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "led_turn_off.log")


# Налаштування логування для вимкнення
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8",
        ),
        logging.StreamHandler(),  # Залишаємо вивід у консоль також
    ],
)

load_dotenv(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".env",
    )
)

MAC_ADDRESS = os.getenv("MAC_ADDRESS")
CHARACTERISTIC_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"
CMD_OFF = bytearray([0x7E, 0x04, 0x04, 0x00, 0x00, 0x00, 0xFF, 0x00, 0xEF])


async def turn_off_led():
    max_retries = 3  # Кількість спроб вимкнення
    for attempt in range(max_retries):
        logging.info(
            "Спроба вимкнення %s з %s. Підключаюся до %s...",
            attempt + 1,
            max_retries,
            MAC_ADDRESS,
        )
        try:
            # Збільшено таймаут на підключення для надійності
            async with BleakClient(MAC_ADDRESS, timeout=15.0) as client:
                if client.is_connected:
                    logging.info("Підключено! Відправляю команду на off...")
                    # Відправка команди без очікування відповіді
                    # (response=False)
                    await client.write_gatt_char(
                        CHARACTERISTIC_UUID, CMD_OFF, response=False
                    )
                    # Даємо час адаптеру передати байти
                    # перед закриттям з'єднання
                    await asyncio.sleep(0.3)
                    logging.info("Стрічку вимкнено успішно.")
                    return True  # Якщо успішно, виходимо з функції
        except Exception:
            logging.exception("Помилка під час спроби %s", attempt + 1)
            if attempt < max_retries - 1:
                logging.info("Чекаю 2 секунди перед наступною спробою...")
                await asyncio.sleep(2)  # Затримка перед повторною спробою

    logging.error("Не вдалося вимкнути стрічку після всіх спроб.")
    return False


if __name__ == "__main__":
    asyncio.run(turn_off_led())
