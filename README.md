# Atom Voice Assistant 🎙️

Atom is a custom, Python-based voice assistant powered by Groq's fast Llama-3 API. It is designed to listen for specific wake words, process natural language commands, and respond using text-to-speech with a friendly, conversational Indian English persona. 

## Features
* **Custom Wake Words**: Wakes up to phrases like "atom", "atom bhai", or "sun atom".
* **State Management**: Enters "Awake" mode upon hearing the wake word and goes to "Sleep" when dismissed.
* **Fast AI Responses**: Uses Groq's `llama-3.3-70b-versatile` model for high-speed, intelligent replies.
* **Text-to-Speech**: Uses local `pyttsx3` for immediate audio feedback.
* **Auto-Sanitization**: Strips emojis and markdown from AI responses to prevent text-to-speech crashes.

## Prerequisites
Before running Atom, ensure you have the following installed:
* Python 3.x
* A valid Groq API Key
* A working microphone

## Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Navtez-Singh/atom.git](https://github.com/Navtez-Singh/atom.git)
   cd atom
