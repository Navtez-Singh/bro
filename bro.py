import speech_recognition as sr
import pyttsx3
from groq import Groq
from datetime import datetime
import time

# --- CONFIGURATION ---
# ⚠️ SECURITY: Never share this key. Use a new one since the old one was exposed.
API_KEY = "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" 

try:
    client = Groq(api_key=API_KEY)
except Exception as e:
    print(f"Failed to initialize Groq: {e}")

# --- 1. VOICE SETUP ---
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# Typically index 0 is Microsoft David (Male) on Windows
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 180) 

def speak(text):
    """Local Text-to-Speech"""
    print(f"Bro: {text}")
    engine.say(text)
    engine.runAndWait()

# --- 2. AI BRAIN ---
def get_ai_response(question):
    """Fetches response from Groq Llama 3"""
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are Bro, a helpful male voice assistant. Give concise 2-sentence answers in a casual, friendly 'bro' tone. Use slang like 'dude' or 'man' occasionally."},
                {"role": "user", "content": question}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"My brain is lagging, bro. Error: {str(e)}"

# --- 3. CORE LOGIC ---
def run_bro():
    recognizer = sr.Recognizer()
    # Boost sensitivity for better wake-word detection
    recognizer.dynamic_energy_threshold = True 
    
    print("\n" + "="*60)
    print("🚀 BRO Voice Assistant is ONLINE")
    print("="*60)
    speak("I'm up! Just say my name if you need anything.")

    with sr.Microphone() as source:
        while True:
            try:
                # Adjust for noise every loop to keep it sharp
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("\n[Listening...]")
                
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
                input_text = recognizer.recognize_google(audio).lower()

                if "bro" in input_text:
                    # Logic: Check if there is a command AFTER the word 'bro'
                    # e.g., "Bro, what time is it?" vs just "Bro"
                    command = input_text.split("bro")[-1].strip()

                    if not command:
                        speak("Yeah bro? What's up?")
                        # Listen specifically for the follow-up
                        audio_cmd = recognizer.listen(source, timeout=5, phrase_time_limit=8)
                        command = recognizer.recognize_google(audio_cmd).lower()
                    
                    print(f"🗣️ You: {command}")

                    # --- COMMAND PROCESSING ---
                    # 1. Exit
                    if any(word in command for word in ['exit', 'goodbye', 'stop', 'quit']):
                        speak("Peace out, bro! Catch you later.")
                        break

                    # 2. Time/Date
                    elif 'time' in command:
                        speak(f"It's currently {datetime.now().strftime('%I:%M %p')}, man.")
                    elif 'date' in command or 'today' in command:
                        speak(f"Today is {datetime.now().strftime('%B %d, %Y')}.")

                    # 3. AI Response
                    else:
                        print("⚙️ Bro is thinking...")
                        ai_msg = get_ai_response(command)
                        speak(ai_msg)

            except sr.UnknownValueError:
                # Ignore background noise that doesn't sound like words
                continue
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                print(f"System Error: {e}")
                continue

if __name__ == "__main__":
    run_bro()