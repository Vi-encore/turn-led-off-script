import asyncio
import logging
import os
from bleak import BleakClient
from dotenv import load_dotenv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "led_turn_on.log")

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

# HEX-команда на ВВІМКНЕННЯ (четвертий байт змінено на 0x01)
CMD_ON = bytearray([0x7E, 0x04, 0x04, 0x01, 0x00, 0x00, 0xFF, 0x00, 0xEF])


async def turn_on_led():
    max_retries = 3  # Кількість спроб вимкнення
    for attempt in range(max_retries):
        logging.info(
            "Спроба підключення %s з %s: Підключаюся до %s...",
            attempt,
            max_retries,
            MAC_ADDRESS,
        )
        try:
            # Збільшила таймаут до 10 секунд, щоб у Bluetooth
            # було більше часу на пошук
            async with BleakClient(MAC_ADDRESS, timeout=10.0) as client:
                if client.is_connected:
                    logging.info(
                        "Підключено! Відправляю команду на ввімкнення..."
                    )

                    # Додано response=False для уникнення помилок
                    # при розриві з'єднання
                    await client.write_gatt_char(
                        CHARACTERISTIC_UUID, CMD_ON, response=False
                    )
                    await asyncio.sleep(0.3)

                    logging.info("Стрічку успішно ввімкнено.")
        except Exception as e:
            logging.error(f"Помилка під час спроби {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                logging.info("Чекаю 2 секунди перед наступною спробою...")
                await asyncio.sleep(2)  # Затримка перед повторною спробою

    logging.error("Не вдалося вимкнути стрічку після всіх спроб.")


if __name__ == "__main__":
    asyncio.run(turn_on_led())
