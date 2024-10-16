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

## Creating an Executable

You can create a standalone executable of this application using PyInstaller. This allows you to run the application without needing Python installed on the target machine.

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```

2. Navigate to the project directory:
   ```
   cd path/to/inline-translator
   ```

3. Create the executable:
   ```
   pyinstaller --onefile --windowed --add-data ".env:." --name inlinetranslator main.py
   ```

4. The executable will be created in the `dist` folder within your project directory.

Note: Make sure all required files (like the .env file) are in the same directory as the executable when distributing it.


## Demo
![Real-Time Translator Demo](./imgs/demo.gif)