# 📱 Mobile Forensic Triage GUI

Welcome to **Mobile Forensic Triage**, a smart, user-friendly desktop tool designed for forensic investigators, ethical hackers, and mobile data analysts.

With this tool, you can connect any Android device via ADB, explore its internal storage (starting from `/sdcard`), preview files and folders, extract specific or full datasets, and export them in neat formats like PDF or CSV.

---

## ✨ Features

* 🔌 **Detect Android Devices** via ADB
* 📂 **Browse Internal Storage** like a file explorer
* 👁️ **Preview Files** (Call Logs, SMS, WhatsApp, Photos, Videos)
* 💾 **Selective or Bulk Extraction** of data
* 📄 **Export Results** to PDF or CSV
* 🌙 **Dark Mode** for night owls and minimalists

---

## ⚙️ Requirements

* **Python 3.6+**
* **ADB (Android Debug Bridge)** installed and available in PATH

### Python Dependencies

```
PyQt5>=5.15.4
reportlab>=3.6.12
```

Install them easily via pip:

```bash
pip install -r requirements.txt
```

---

## 🚀 Getting Started

### 1. **Clone the Project**

```bash
git clone https://github.com/yourusername/mobile-forensic-gui.git
cd mobile-forensic-gui
```

### 2. **Install the Python Requirements**

```bash
pip install -r requirements.txt
```

### 3. **Install ADB**

* **Windows**: Download from [Android developer tools](https://developer.android.com/tools/releases/platform-tools) → Extract → Add to `PATH`
* **Linux**:

  ```bash
  sudo apt install android-tools-adb
  ```
* **macOS**:

  ```bash
  brew install android-platform-tools
  ```

### 4. **Enable USB Debugging on Your Phone**

* Go to `Settings > About phone > Tap 'Build number' 7 times` to enable developer mode.
* Then go to `Developer options > Enable USB Debugging`.

### 5. **Connect Your Device**

Use a USB cable and confirm the debugging permission on your device when prompted.

---

## 💻 Run the App

Once everything’s set:

```bash
python main.py
```

You’ll see a GUI pop up where you can:

* Detect your device
* Navigate through folders
* Double-click to preview files
* Extract files or folders
* Export data to PDF or CSV

---

## 💡 Tip for Use

* Use the **checklist** on the left to navigate folders
* **Double-click** files in the table to select them for extraction
* Use the **back** button to return to previous directories

---

## 🙌 Contributing

Pull requests are welcome! If you spot a bug or have a cool feature idea, don’t hesitate to open an issue or fork the project.

---

## 🛡️ Disclaimer

This tool is intended for **educational** and **authorized forensic investigations only**. Use responsibly and with consent.

---

## 📬 Contact

For feedback or questions, reach out via [GitHub Issues](https://github.com/yourusername/mobile-forensic-gui/issues) 
