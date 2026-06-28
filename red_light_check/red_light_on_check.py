import winreg
import time

# Шлях до бінарного ключа нічного світла в реєстрі Windows
REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\CloudStore\Store\DefaultAccount\Current\default$windows.data.bluelightreduction.bluelightreductionstate\windows.data.bluelightreduction.bluelightreductionstate"


# Функція для перевірки стану нічника
def is_night_light_on():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH) as key:
            data, _ = winreg.QueryValueEx(key, "Data")

            # Windows зберігає стан у складному бінарному вигляді (REG_BINARY).
            # Експериментально доведено, що при активації нічника 23-й байт
            # змінює своє значення на 0x10 або 0x13.
            if len(data) > 23 and data[23] in [0x10, 0x13]:
                return True
            return False
    except Exception as e:
        print(f"Не вдалося зчитати реєстр: {e}")
        return False
