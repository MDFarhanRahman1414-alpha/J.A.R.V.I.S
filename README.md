# J.A.R.V.I.S
🔥 JARVIS – Local AI Voice Assistant

A high-performance offline+online AI assistant that listens, understands, and performs tasks in real time.

✨ Features
🎤 Speech Recognition (STT) – Real-time voice command capture
🗣️ Text-to-Speech (TTS) – Natural AI responses
🌐 Realtime Browser Control – Search, open tabs, automate actions
🧠 Modular Command Handler – Add unlimited custom commands
⚙️ Local + Cloud Hybrid – Works offline with local models
🪟 Frontend Interface – Clean local dashboard (index.html)

📁 Folder Structure
JARVIS/
│
├── frontend/
│   └── index.html
│
├── src/
│   ├── jarvis.py
│   ├── stt.py
│   ├── tts.py
│   ├── commands.py
│   ├── realtime.py
│   ├── utils.py
│
├── assets/
│   └── jarvis.png     # UI image (add yours here)
│
├── requirements.txt
├── .gitignore
└── README.md

⚙️ Installation

1. Clone the repository
git clone https://github.com/your-username/JARVIS.git
cd JARVIS

3. Install dependencies
   
pip install -r requirements.txt
▶️ Usage

Run the main controller:

python src/jarvis.py

🧩 Add ChromeDriver Manually (Required)

Because GitHub does not allow .exe uploads, download the driver yourself:

Download:
https://chromedriver.chromium.org/downloads

Place it here:

JARVIS/Backend/Drivers/chromedriver.exe

🤝 Contributing


Pull requests are welcome. For major changes, open an issue first.

![J.A.R.V.I.S Dashboard](JARVIS/assets/JARVIS/assets/jarvis%20interface.PNG)
