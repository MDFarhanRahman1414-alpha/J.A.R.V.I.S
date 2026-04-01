import edge_tts
import asyncio
import random
import os
import tempfile
from playsound import playsound

# Friendly, witty, humorous voice
VOICE = "en-US-BrianNeural"
RATE  = "+0%"
PITCH = "-5Hz"

# Predefined responses when text is too long
responses = [
    "The rest of the result has been printed to the chat screen, kindly check it out sir.",
    "The rest of the text is now on the chat screen, sir, please check it.",
    "You can see the rest of the text on the chat screen, sir.",
    "The remaining part of the text is now on the chat screen, sir.",
    "Sir, you'll find more text on the chat screen for you to see.",
    "The rest of the answer is now on the chat screen, sir.",
    "Sir, please look at the chat screen, the rest of the answer is there.",
    "You'll find the complete answer on the chat screen, sir.",
    "The next part of the text is on the chat screen, sir.",
    "Sir, please check the chat screen for more information.",
    "There's more text on the chat screen for you, sir.",
    "Sir, take a look at the chat screen for additional text.",
    "You'll find more to read on the chat screen, sir.",
    "Sir, check the chat screen for the rest of the text.",
    "The chat screen has the rest of the text, sir.",
    "There's more to see on the chat screen, sir, please look.",
    "Sir, the chat screen holds the continuation of the text.",
    "You'll find the complete answer on the chat screen, kindly check it out sir.",
    "Please review the chat screen for the rest of the text, sir.",
    "Sir, look at the chat screen for the complete answer.",
]


def TTS(text, func=lambda r=None: True):
    asyncio.run(_tts_async(text))


async def _tts_async(text):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            temp_file = f.name

        communicate = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH)
        await communicate.save(temp_file)

        # playsound plays the file and waits until done
        playsound(temp_file)

        os.remove(temp_file)

    except Exception as e:
        print(f"TTS Error: {e}")


def TextToSpeech(text, func=lambda r=None: True):
    """
    If text is too long (4+ sentences and 250+ chars),
    speak only first 2 sentences + redirect message.
    Otherwise speak the whole thing.
    """
    data = str(text).split(".")

    if len(data) > 4 and len(text) >= 250:
        TTS(". ".join(text.split(".")[0:2]) + ". " + random.choice(responses), func)
    else:
        TTS(text, func)


if __name__ == "__main__":
    print("Testing JARVIS voice...")
    TextToSpeech(
        "Hello sir, I am JARVIS, your personal AI assistant. "
        "I am online and fully operational. How may I assist you today?"
    )
    print("Done.")




