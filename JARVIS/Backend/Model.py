import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from cohere import ClientV2

client = ClientV2("")

SYSTEM_PROMPT = """You are JARVIS's decision-making brain.
Classify the user's query into task types.

Reply ONLY with a comma-separated list using these exact task types:
general, realtime, open, close, play, google search, youtube search, reminder, system, exit

Rules:
- general        → questions, facts, conversations
- realtime       → news, weather, live scores, current prices
- open           → open an app  e.g. open (chrome)
- close          → close an app e.g. close (chrome)
- play           → play a song  e.g. play (starboy)
- google search  → e.g. google search (python tutorials)
- youtube search → e.g. youtube search (lofi music)
- reminder       → e.g. reminder (10 drink water)
- system         → volume, brightness, shutdown, restart
- exit           → goodbye, quit, shut down jarvis

Examples:
User: What is gravity?                    → general
User: What is the news today?             → realtime
User: Open Chrome                         → open (chrome)
User: Play Starboy                        → play (starboy)
User: Search cats on YouTube             → youtube search (cats)
User: Remind me in 5 mins to drink water → reminder (5 drink water)
User: Open Chrome and play Starboy       → open (chrome), play (starboy)
User: Goodbye                            → exit

Return ONLY the task list. No explanation. No extra text."""


def FirstLayerDMM(prompt: str) -> list:
    try:
        response = client.chat(
            model="command-a-03-2025",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt}
            ]
        )
        raw = response.message.content[0].text.strip()
        tasks = [t.strip() for t in raw.split(",") if t.strip()]
        return tasks if tasks else ["general"]

    except Exception as e:
        print(f"[Model Error] {e}")
        return ["general"]


if __name__ == "__main__":
    print("Model.py — Test Mode\n")
    while True:
        try:
            q = input(">>> ").strip()
            if q in ["exit", "quit"]: break
            print(f"→ {FirstLayerDMM(q)}\n")
        except KeyboardInterrupt:
            break