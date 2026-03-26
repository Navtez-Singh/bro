import speech_recognition as sr
import pyttsx3
from groq import Groq
from datetime import datetime
import re

# --- CONFIGURATION ---
API_KEY = "YOUR_NEW_API_KEY_HERE" 
client = Groq(api_key=API_KEY)

# --- VOICE SETUP ---
engine = pyttsx3.init()
voices = engine.getProperty('voices')

voice_found = False
for voice in voices:
    name = voice.name.lower()
    if "david" in name or "ravi" in name or "mark" in name:
        engine.setProperty('voice', voice.id)
        voice_found = True
        break

if not voice_found and len(voices) > 1:
    engine.setProperty('voice', voices[1].id)

engine.setProperty('rate', 180) 

def speak(text):
    clean_text = re.sub(r'[^\w\s.,!?\'"-]', '', text)
    print(f"Atom: {clean_text}")
    engine.say(clean_text)
    engine.runAndWait()

# --- AI LOGIC ---
def get_ai_response(question):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are Atom, a helpful voice assistant. Give concise 2-sentence answers. Address the user as 'sir', 'my friend', or 'friend'. You can use casual Indian English slang like 'yaar', 'bhai', or 'scene kya hai', but NEVER use the word 'boss'. Do NOT use emojis or special characters."},
                {"role": "user", "content": question}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Connection error, my friend."

# --- CORE SYSTEM ---
def run_atom():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 400 
    recognizer.dynamic_energy_threshold = False 
    
    wake_words = ["atom", "atom bhai", "sun atom", "bol atom", "aur atom", "atom yaar"]
    close_words = ["bye", "ok bye", "thanks", "exit", "stop", "chalo bye"]
    
    is_awake = False 

    print("\n" + "="*50)
    print("🚀 ATOM Voice Assistant is ONLINE (Standby Mode)")
    print("="*50)

    with sr.Microphone() as source:
        print("[Calibrating microphone for 1 second...]")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        while True:
            try:
                state = "AWAKE" if is_awake else "ASLEEP"
                print(f"\n[{state}] Listening...")
                
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=8)
                input_text = recognizer.recognize_google(audio).lower()
                print(f"Heard: '{input_text}'")

                # --- CHECK FOR EXIT COMMAND FIRST ---
                # This ensures the program closes immediately whether asleep or awake
                if any(word in input_text for word in close_words):
                    speak("Goodbye my friend. Shutting down system now.")
                    break # <--- This command completely kills the loop and script
                
                # --- IF ASLEEP ---
                if not is_awake:
                    for word in wake_words:
                        if word in input_text:
                            is_awake = True
                            
                            command = input_text.split(word, 1)[-1].strip()
                            
                            if command:
                                if 'time' in command:
                                    speak(f"It's {datetime.now().strftime('%I:%M %p')}.")
                                elif 'date' in command or 'today' in command:
                                    speak(f"Today is {datetime.now().strftime('%B %d, %Y')}.")
                                else:
                                    speak(get_ai_response(command))
                            else:
                                speak("Haan bhai, tell me.")
                            break 

                # --- IF AWAKE ---
                else:
                    if 'time' in input_text:
                        speak(f"It's {datetime.now().strftime('%I:%M %p')}.")
                    elif 'date' in input_text or 'today' in input_text:
                        speak(f"Today is {datetime.now().strftime('%B %d, %Y')}.")
                    else:
                        print("Fetching AI response...")
                        speak(get_ai_response(input_text))

            except sr.UnknownValueError:
                pass 
            except sr.RequestError as e:
                print(f"Network Error: {e}")
            except sr.WaitTimeoutError:
                pass
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    run_atom()
    
