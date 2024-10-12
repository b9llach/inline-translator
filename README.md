# Real-Time Translator

This application provides real-time translation capabilities, including text input translation, screen capture OCR translation, and a graphical user interface for easy control.

## Features

- Real-time text translation as you type
- Screen capture and OCR translation
- Support for multiple languages
- User-friendly GUI for easy control and language selection
- Hotkey support for quick toggling and screen capture

## Requirements

- Python 3.7+
- PyQt6
- deep_translator
- pyautogui
- pyperclip
- gTTS
- playsound
- Pillow
- pynput
- requests
- python-dotenv

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/b9llach/inline-translator.git
   cd inline-translator
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your OCR Space API key:
   ```
   KEY=your_ocr_space_api_key_here
   ```

## Usage

1. Run the main script:
   ```
   python main.py
   ```

2. Use the GUI to select your target language and control translation settings.

3. Type anywhere on your system to see real-time translations.

4. Use F9 to toggle translation on/off.

5. Use F10 to capture a screen area for OCR translation.

## Files

- `main.py`: Entry point of the application
- `translator.py`: Core translation logic
- `gui.py`: Graphical user interface
- `screen_capture.py`: Screen capture functionality
- `keyboard_input.py`: Keyboard input handling

## Demo

![Real-Time Translator Demo](./imgs/demo.gif)