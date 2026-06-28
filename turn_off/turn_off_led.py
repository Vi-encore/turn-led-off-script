import asyncio
import logging
import os
from bleak import BleakClient, BleakError
from dotenv import load_dotenv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "led_turn_off.log")
LOGGER = logging.getLogger("led_turn_off")
LOGGER.setLevel(logging.INFO)
LOGGER.propagate = False


# Налаштування логування для вимкнення
# Очищуємо старі обробники, щоб уникнути дублювання
for handler in LOGGER.handlers[:]:
    LOGGER.removeHandler(handler)

if not LOGGER.handlers:
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    LOGGER.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    LOGGER.addHandler(stream_handler)

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
        LOGGER.info(
            "Спроба вимкнення %s з %s. Підключаюся до %s...",
            attempt + 1,
            max_retries,
            MAC_ADDRESS,
        )
        try:
            # Збільшено таймаут на підключення для надійності
            async with BleakClient(MAC_ADDRESS, timeout=15.0) as client:
                if client.is_connected:
                    LOGGER.info("Підключено! Відправляю команду на off...")
                    # Відправка команди без очікування відповіді
                    # (response=False)
                    await client.write_gatt_char(
                        CHARACTERISTIC_UUID, CMD_OFF, response=False
                    )
                    # Даємо час адаптеру передати байти
                    # перед закриттям з'єднання
                    await asyncio.sleep(0.3)
                    LOGGER.info("Стрічку вимкнено успішно.")
                    return True  # Якщо успішно, виходимо з функції
        except BleakError as e:
            LOGGER.error("Помилка під час спроби %s: %s", attempt + 1, str(e))
            if attempt < max_retries - 1:
                LOGGER.info("Чекаю 2 секунди перед наступною спробою...")
                await asyncio.sleep(2)  # Затримка перед повторною спробою

    LOGGER.error("Не вдалося вимкнути стрічку після всіх спроб.")
    return False


if __name__ == "__main__":
    asyncio.run(turn_off_led())
