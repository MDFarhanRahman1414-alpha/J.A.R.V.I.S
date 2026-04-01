import os
import json
import time
import webbrowser
import threading
import subprocess
from datetime import datetime

# =====================================================
# ================ APP PATHS ==========================
# =====================================================

APPS = {
    "notepad":       "notepad.exe",
    "chrome":        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "vs code":       "code",
    "file explorer": "explorer.exe",
    "calculator":    "calc.exe",
    "task manager":  "taskmgr.exe",
    "word":          "winword.exe",
    "excel":         "excel.exe",
    "paint":         "mspaint.exe",
    "cmd":           "cmd.exe",
    "powershell":    "powershell.exe",
    "spotify":       "spotify.exe",
    "discord":       "discord.exe",
    "whatsapp":      "whatsapp.exe",
    "telegram":      "telegram.exe",
    "vlc":           "vlc.exe",
}

# =====================================================
# ================ OPEN APP ===========================
# =====================================================

def OpenApp(app_name):
    app = app_name.lower().strip()

    if app in APPS:
        try:
            subprocess.Popen(APPS[app])
            return f"Opening {app_name}, sir."
        except Exception as e:
            return f"Could not open {app_name}: {e}"

    # Website detection
    if "." in app or app.startswith("www"):
        url = f"https://{app}" if not app.startswith("http") else app
        webbrowser.open(url)
        return f"Opening {app_name} in browser, sir."

    # Last resort — try as raw command
    try:
        subprocess.Popen(app)
        return f"Opening {app_name}, sir."
    except:
        return f"Sorry sir, I couldn't find {app_name}."


# =====================================================
# ================ CLOSE APP ==========================
# =====================================================

def CloseApp(app_name):
    app = app_name.lower().strip()
    process_map = {
        "notepad":    "notepad.exe",
        "chrome":     "chrome.exe",
        "vs code":    "Code.exe",
        "word":       "winword.exe",
        "excel":      "excel.exe",
        "paint":      "mspaint.exe",
        "spotify":    "Spotify.exe",
        "discord":    "Discord.exe",
        "vlc":        "vlc.exe",
        "telegram":   "Telegram.exe",
    }
    process = process_map.get(app, app + ".exe")
    try:
        result = os.system(f"taskkill /im {process} /f")
        if result == 0:
            return f"Closed {app_name}, sir."
        else:
            return f"{app_name} was not running, sir."
    except Exception as e:
        return f"Could not close {app_name}: {e}"


# =====================================================
# ================ YOUTUBE / SEARCH ===================
# =====================================================

def PlayYoutube(query):
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Playing {query} on YouTube, sir."


def GoogleSearch(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Searching Google for {query}, sir."


def YoutubeSearch(query):
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Searching YouTube for {query}, sir."


# =====================================================
# ================ SYSTEM CONTROLS ====================
# =====================================================

def SystemControl(command):
    command = command.lower().strip()

    if "shutdown" in command:
        os.system("shutdown /s /t 5")
        return "Shutting down your PC in 5 seconds, sir."

    elif "restart" in command:
        os.system("shutdown /r /t 5")
        return "Restarting your PC in 5 seconds, sir."

    elif "sleep" in command or "hibernate" in command:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Putting your PC to sleep, sir."

    elif "lock" in command:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Locking your PC, sir."

    elif "volume up" in command:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            current = volume.GetMasterVolumeLevelScalar()
            volume.SetMasterVolumeLevelScalar(min(1.0, current + 0.1), None)
            return "Volume increased, sir."
        except:
            return "Could not adjust volume, sir."

    elif "volume down" in command:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            current = volume.GetMasterVolumeLevelScalar()
            volume.SetMasterVolumeLevelScalar(max(0.0, current - 0.1), None)
            return "Volume decreased, sir."
        except:
            return "Could not adjust volume, sir."

    elif "mute" in command:
        os.system("nircmd.exe mutesysvolume 1")
        return "System muted, sir."

    else:
        return f"System command not recognized: {command}"


# =====================================================
# ================ REMINDER ENGINE ====================
# =====================================================

reminder_list = []

def SetReminder(minutes, message):
    try:
        trigger_time = datetime.now().timestamp() + float(minutes) * 60
        reminder_list.append({"time": trigger_time, "msg": message})
        return f"Reminder set for {minutes} minutes, sir. I'll remind you: {message}"
    except Exception as e:
        return f"Could not set reminder: {e}"


def _reminder_loop():
    while True:
        now = datetime.now().timestamp()
        for r in reminder_list[:]:
            if now >= r["time"]:
                print(f"\n⏰ REMINDER: {r['msg']}")
                try:
                    from Backend.TextToSpeech import TextToSpeech
                    TextToSpeech(f"Sir, your reminder: {r['msg']}")
                except:
                    pass
                reminder_list.remove(r)
        time.sleep(1)

threading.Thread(target=_reminder_loop, daemon=True).start()


# =====================================================
# ================ CALENDAR ===========================
# =====================================================

CALENDAR_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data", "Calendar.json")

def _load_calendar():
    if not os.path.exists(CALENDAR_FILE):
        return []
    with open(CALENDAR_FILE, "r") as f:
        return json.load(f)

def _save_calendar(data):
    with open(CALENDAR_FILE, "w") as f:
        json.dump(data, f, indent=4)

def AddEvent(date, time_str, message):
    events = _load_calendar()
    events.append({"date": date, "time": time_str, "msg": message})
    _save_calendar(events)
    return f"Event added: {message} on {date} at {time_str}, sir."

def ShowTodayEvents():
    events = _load_calendar()
    today = datetime.now().strftime("%Y-%m-%d")
    today_events = [e for e in events if e["date"] == today]
    if not today_events:
        return "You have no events scheduled for today, sir."
    result = "Your events for today:\n"
    for e in today_events:
        result += f"  • {e['time']} — {e['msg']}\n"
    return result.strip()

def _calendar_notifier():
    while True:
        now = datetime.now()
        events = _load_calendar()
        for e in events:
            if (e["date"] == now.strftime("%Y-%m-%d") and
                    e["time"] == now.strftime("%H:%M")):
                try:
                    from Backend.TextToSpeech import TextToSpeech
                    TextToSpeech(f"Sir, calendar reminder: {e['msg']}")
                except:
                    pass
                time.sleep(60)
        time.sleep(1)

threading.Thread(target=_calendar_notifier, daemon=True).start()


# =====================================================
# ================ MAIN ROUTER ========================
# =====================================================

def Automation(tasks: list) -> list:
    results = []

    for task in tasks:
        task_original = task.strip()
        task = task.strip().lower()

        try:
            # --- OPEN ---
            if task.startswith("open"):
                target = task.replace("open", "").replace("(", "").replace(")", "").strip()
                results.append(OpenApp(target))

            # --- CLOSE ---
            elif task.startswith("close"):
                target = task.replace("close", "").replace("(", "").replace(")", "").strip()
                results.append(CloseApp(target))

            # --- PLAY ---
            elif task.startswith("play"):
                query = task.replace("play", "").replace("(", "").replace(")", "").strip()
                results.append(PlayYoutube(query))

            # --- GOOGLE SEARCH ---
            elif task.startswith("google search"):
                query = task.replace("google search", "").replace("(", "").replace(")", "").strip()
                results.append(GoogleSearch(query))

            # --- YOUTUBE SEARCH ---
            elif task.startswith("youtube search"):
                query = task.replace("youtube search", "").replace("(", "").replace(")", "").strip()
                results.append(YoutubeSearch(query))

            # --- SYSTEM ---
            elif task.startswith("system"):
                command = task.replace("system", "").replace("(", "").replace(")", "").strip()
                results.append(SystemControl(command))

            # --- REMINDER ---
            elif task.startswith("reminder"):
                inside = task.replace("reminder", "").replace("(", "").replace(")", "").strip()
                parts = inside.split(" ", 1)
                mins = parts[0]
                msg  = parts[1] if len(parts) > 1 else "reminder"
                results.append(SetReminder(mins, msg))

            # --- CALENDAR ADD ---
            elif task.startswith("add event"):
                inside = task.replace("add event", "").replace("(", "").replace(")", "").strip()
                date, time_str, msg = [x.strip() for x in inside.split(",")]
                results.append(AddEvent(date, time_str, msg))

            # --- CALENDAR SHOW ---
            elif "today" in task and "event" in task:
                results.append(ShowTodayEvents())

            else:
                results.append(f"Command not recognized: {task}")

        except Exception as e:
            results.append(f"Error executing '{task}': {e}")

    return results


# =====================================================
# ================ TERMINAL TEST MODE =================
# =====================================================

if __name__ == "__main__":
    print("Automation.py — Terminal Test Mode")
    print("Try: open chrome | play starboy | reminder 5 drink water\n")
    while True:
        try:
            cmd = input(">>> ").strip()
            if cmd in ["exit", "quit"]: break
            results = Automation([cmd])
            for r in results:
                print(f"→ {r}")
        except KeyboardInterrupt:
            print("\nExiting.")
            break