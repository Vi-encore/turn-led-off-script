import asyncio
from bleak import BleakScanner


async def scan_devices():
    print("Шукаю Bluetooth пристрої поруч...")
    devices = await BleakScanner.discover()
    for d in devices:
        # Шукаємо пристрої, які хоч трохи схожі на лед-стрічку
        if d.name and (
            "elk" in d.name.lower()
            or "bledom" in d.name.lower()
            or "triones" in d.name.lower()
            or "led" in d.name.lower()
        ):
            print(f"Знайдено стрічку! Назва: {d.name}, MAC-адреса: {d.address}")
        else:
            print(f"Інший пристрій: {d.name} - {d.address}")


if __name__ == "__main__":
    asyncio.run(scan_devices())
