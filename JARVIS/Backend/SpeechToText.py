import whisper
import speech_recognition as sr
import os

# Load the model (tiny is fast, base is balanced, large is most accurate)
model = whisper.load_model("base")

def jarvis_whisper_listen():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Jarvis is listening (Whisper Mode)...")
        audio = recognizer.listen(source)
        
        # Save audio to a temporary file
        with open("temp_audio.wav", "wb") as f:
            f.write(audio.get_wav_data())

    # Transcribe using Whisper
    result = model.transcribe("temp_audio.wav")
    text = result["text"].strip()
    
    print(f"Jarvis heard: {text}")
    
    # Cleanup temp file
    os.remove("temp_audio.wav")
    return text.lower()

if __name__ == "__main__":
    jarvis_whisper_listen()