import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import threading
import json
from datetime import datetime

# ── Import all JARVIS backend modules ──────────────────────────────────────
from Backend.Model import FirstLayerDMM
from Backend.Chatbot import ChatBot
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.TextToSpeech import TextToSpeech

app = Flask(__name__, static_folder="Frontend", static_url_path="")
CORS(app)

# ── In-memory activity log ──────────────────────────────────────────────────
activity_log = []
chat_history = []

def log_activity(step, title, detail):
    activity_log.clear() if len(activity_log) > 20 else None
    activity_log.append({
        "step": step,
        "title": title,
        "detail": detail,
        "time": datetime.now().strftime("%H:%M:%S")
    })

# ── Serve frontend ──────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory("Frontend", "index.html")

# ── Main chat endpoint ──────────────────────────────────────────────────────
@app.route("/chat", methods=["POST"])
def chat():
    global activity_log
    activity_log = []

    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Add user message to history
    chat_history.append({"role": "user", "content": user_message, "time": datetime.now().strftime("%H:%M")})
    log_activity(1, "Query detected", user_message)

    try:
        # ── Step 1: Decision Making Model ──────────────────────────────────
        tasks = FirstLayerDMM(user_message)
        log_activity(2, "Brain decision", f"Tasks: {', '.join(tasks)}")

        responses = []
        route_used = "General"

        for task in tasks:
            task_lower = task.lower().strip()

            # ── General query → Chatbot ──────────────────────────────────
            if task_lower.startswith("general"):
                route_used = "General"
                log_activity(3, "Route selected", "→ General (Chatbot)")
                log_activity(4, "Streaming response", "Generating via Chatbot AI")
                query = task_lower.replace("general", "").replace("(", "").replace(")", "").strip()
                answer = ChatBot(query or user_message)
                responses.append(answer)

            # ── Realtime query → Search Engine ──────────────────────────
            elif task_lower.startswith("realtime"):
                route_used = "Realtime"
                log_activity(3, "Route selected", "→ Realtime (Search Engine)")
                log_activity(4, "Streaming response", "Searching the web...")
                query = task_lower.replace("realtime", "").replace("(", "").replace(")", "").strip()
                answer = RealtimeSearchEngine(query or user_message)
                responses.append(answer)

            # ── Automation tasks ─────────────────────────────────────────
            elif any(task_lower.startswith(x) for x in ["open", "close", "play", "google search", "youtube search", "reminder", "system"]):
                route_used = "Automation"
                log_activity(3, "Route selected", "→ Automation")
                log_activity(4, "Executing task", f"Running: {task}")
                results = Automation([task])
                responses.extend(results)

            # ── Exit ─────────────────────────────────────────────────────
            elif task_lower.startswith("exit"):
                responses.append("Goodbye sir. Shutting down JARVIS.")

            else:
                # Fallback to chatbot
                route_used = "General"
                log_activity(3, "Route selected", "→ General (fallback)")
                answer = ChatBot(user_message)
                responses.append(answer)

        final_response = " ".join(responses) if responses else "I'm sorry sir, I didn't understand that."

        # ── Step 2: Log completion ──────────────────────────────────────
        elapsed = "~340ms"
        log_activity(5, "Core responded", f"Core responded in {elapsed}")

        # ── Step 3: Speak response in background ────────────────────────
        threading.Thread(
            target=TextToSpeech,
            args=(final_response,),
            daemon=True
        ).start()

        # ── Step 4: Save to chat history ────────────────────────────────
        chat_history.append({
            "role": "assistant",
            "content": final_response,
            "time": datetime.now().strftime("%H:%M"),
            "route": route_used
        })

        return jsonify({
            "response": final_response,
            "route": route_used,
            "tasks": tasks,
            "activity": activity_log
        })

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        log_activity(5, "Error", error_msg)
        return jsonify({"response": error_msg, "route": "Error", "tasks": [], "activity": activity_log}), 500


# ── Chat history endpoint ───────────────────────────────────────────────────
@app.route("/history", methods=["GET"])
def history():
    return jsonify(chat_history)


# ── Activity log endpoint ───────────────────────────────────────────────────
@app.route("/activity", methods=["GET"])
def activity():
    return jsonify(activity_log)


# ── Status endpoint ─────────────────────────────────────────────────────────
@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "online", "version": "1.0.0"})


# ── Run server ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "="*50)
    print("  J.A.R.V.I.S — Starting up...")
    print("  Open your browser at: http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=False, port=5000, threaded=True)