# Windows BLE LED Strip Automator

This repository contains Python scripts for controlling a Bluetooth Low Energy (BLE) LED strip, commonly based on the ELK-BLEDOM controller. The project can synchronize the LED strip with the Windows Night Light state and turn it off automatically when needed.

## Project Structure

The repository is organized around the files that already exist in this workspace:

- `main.py`: Main background loop that checks the Windows Night Light state and triggers the LED actions.
- `red_light_check/red_light_on_check.py`: Reads the Windows Registry to detect whether Night Light is enabled.
- `turn_on/turn_on_led.py`: Connects to the BLE strip and sends the command that turns it on.
- `turn_off/turn_off_led.py`: Connects to the BLE strip and sends the command that turns it off.
- `find_mac.py`: Helper script for finding the strip MAC address.

Each script writes its own log file next to the script, for example `turn_on/led_turn_on.log`, `turn_off/led_turn_off.log`, and `sync_night_light.log` in the project root.

## Prerequisites

- Windows 10 or 11.
- Python 3.7 or newer.
- A Bluetooth adapter and a compatible BLE LED strip.

## 🛠 Setup & Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Install the required dependencies:** The scripts use the `bleak` library for Bluetooth communication and `python-dotenv` for environment variables. Install them globally (recommended for Windows background tasks) or in a virtual environment:

   ```bash
   pip install bleak python-dotenv
   ```

3. **Configure Environment Variables:** For security, the MAC Address is not hardcoded.
   - Copy the `.env.example` file and rename it to `.env`.
   - Open the new `.env` file and add your LED strip's MAC address:
   ```
   MAC_ADDRESS=XX:XX:XX:XX:XX:XX
   ```

## ⚙️ How to Use (Background Automation)

Currently, the project is designed to run silently in the background using Windows features.

### 📝 Quick Tip: How to create a `.bat` file

If you haven't created a batch file before, follow these steps:

1. Open Notepad on your PC.
2. Paste the provided code snippets below for the specific task.
3. Click **File → Save As...**
4. Change "Save as type" to **All Files (.\*)** (This is crucial, otherwise it saves as a `.txt` file).
5. Name your file ending with `.bat` (e.g., `start_sync.bat`).
6. Save it in the root folder of this project.

### 1. Night Light Synchronization

To run the monitoring script automatically on startup without a console window, create a `.bat` file (e.g., `sync_night_light.bat`) in the root directory containing:

```bat
@echo off
start "" /B pythonw "C:\path\to\your\project\main.py"
```

Place a shortcut to this `.bat` file in your Windows Startup folder (`Win + R` → `shell:startup`).

### 2. Auto Turn-Off on PC Shutdown

To ensure the LED strip turns off when the computer shuts down, create a `.bat` file (e.g., `turn_off_led.bat`) containing:

```bat
@echo off
python "C:\path\to\your\project\turn_off\turn_off_led.py"
```

Then, use Windows Group Policy to run it on shutdown:

1. Open `gpedit.msc`.
2. Navigate to **Computer Configuration → Windows Settings → Scripts (Startup/Shutdown)**.
3. Double-click on **Shutdown**, click **Add...**, and point it to the `.bat` file you just created.

## 🔮 Future Roadmap (Electron App)

Currently, the scripts run strictly as automated background tasks. However, this repository will soon be upgraded!

I plan to build a **Desktop GUI Application** using **Electron.js**. The future Electron app will serve as a control panel for manual color picking, brightness adjustments, and toggling. It will utilize Node.js `child_process` to seamlessly call these existing Python scripts, combining the reliability of Python's `bleak` on Windows with a modern JavaScript UI. Stay tuned!
