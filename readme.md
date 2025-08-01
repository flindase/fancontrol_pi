# Raspberry Pi Fan Web Controller

A simple web interface for controlling a PWM fan on Raspberry Pi using CPU temperature. Built with Flask, runs automatically at boot using systemd, and allows live control and configuration through your browser.

---

## 🌟 Features

- 🌡️ View live CPU temperature
- 💨 Monitor current fan speed (PWM duty cycle)
- ⚙️ Configure fan speed per temperature threshold
- 🔧 Enable manual override mode
- 🖥️ Displays Raspberry Pi hostname
- 🚀 Runs as a systemd service

---

## 📦 Requirements

- Raspberry Pi 4 (or compatible with GPIO PWM)
- Ubuntu Server (or Raspberry Pi OS)
- 3-wire fan (PWM-compatible, connected to GPIO 14)

---

## 🔧 Installation

### 1. Install Required Packages

```bash
sudo apt update
sudo apt install python3 python3-flask python3-rpi.gpio git
```

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/fan-web.git
cd fan-web
```

### 3. Run Manually (Optional Test)

```bash
python3 app.py
```

Visit `http://<your-pi-ip>:5000` in your browser to test.

---

## ⚙️ Set Up as a systemd Service

### 1. Copy the service file

```bash
sudo cp fan-web.service /etc/systemd/system/
```

> Make sure paths in `fan-web.service` match your system (e.g., `/home/ubuntu/fan-web/app.py`). Sometimes this can be tricky running as non-root (run as root to test if it is not working)

### 2. Enable and Start

```bash
sudo systemctl daemon-reexec
sudo systemctl enable fan-web
sudo systemctl start fan-web
```

### 3. Check Status

```bash
sudo systemctl status fan-web
```

You should see:

```
Active: active (running)
```

---

## 🧪 Default Behavior

When started for the first time, a default `settings.json` will be created automatically:

```json
{
  "temp_thresholds": [
    { "temp": 50, "duty": 70 }
  ],
  "manual_override": false,
  "manual_duty": 60
}
```

---

## 🖥 Web UI Usage

- Shows server hostname (useful for managing multiple Pis)
- View real-time temperature and fan speed
- Set fan speed manually or configure rules like:

```json
"temp_thresholds": [
  { "temp": 40, "duty": 30 },
  { "temp": 50, "duty": 60 },
  { "temp": 60, "duty": 100 }
]
```

---

## 📂 Project Structure

```
fan-web/
├── app.py               # Main app (Flask + GPIO)
├── fan-web.service      # systemd unit file
├── settings.json        # Fan configuration (auto-created)
├── templates/
│   └── index.html       # Web UI template
```

---

## 📜 License

MIT License

---

## 🧠 Future Ideas (PRs welcome!)

- Temperature/Fan logging
- Graphs or dashboards
- REST API
- Mobile UI
  


