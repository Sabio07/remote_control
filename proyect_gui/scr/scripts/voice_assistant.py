import os
import sys
import pyperclip
import pyautogui
import time
from datetime import datetime
import keyboard
import winsound
import pyttsx3
import win32con
import win32gui
import webbrowser
import json
import subprocess
import speech_recognition as sr

sys.path.append("C:")

from DataAdmin import getValueDb


class Voice_Assistant:
    """
    Class representing a voice assistant.

    Attributes:
        username (str): The username of the user of the assistant.
        data_numbers (dict): Data loaded from numbers.json.
        data_settings (dict): Data loaded from settings.json.
        recognizer (sr.Recognizer): Speech recognizer object.
        list_numeros (list): List of numbers from data_numbers.

    Methods:
        main(): Main method to start the voice assistant.
        execute_commands(command): Executes commands given to the assistant.
        beep(frequency, duration, state=True): Emits a sound if state is True.
        read_text(text, volumen=1.0, state=True): Reads out the text if state is True.
        minimize_window(): Minimizes the active window.
        maximize_window(): Maximizes the active window.
        listen_commands(): Listens to user commands using the microphone.
    """

    def __init__(self, username):
        """
        Initialize the self.Voice_Assistant object.

        Args:
            username (str): The username of the user.
        """
        self.username = username

        with open("scr/scripts/numbers.json", 'r') as numbers_list_json:
            self.data_numbers = json.load(numbers_list_json)

        with open("settings.json", 'r') as settings_json:
            self.data_settings = json.load(settings_json)
        
        self.list_numeros = self.data_numbers["numeros"]

        self.recognizer = sr.Recognizer()

        self.main()
    
    def main(self):
        """
        Main method to start the voice assistant.
        """

        # Get the values for the user in the user's db
        self.voice = getValueDb(f"settings_{self.username}", "Service", "voice", "State")
        self.sound = getValueDb(f"settings_{self.username}", "Service", "sound", "State")
        self.volumen_user = getValueDb(f"settings_{self.username}", "Service", "volumen_user", "State")
        self.writing_speed = getValueDb(f"settings_{self.username}", "Service", "writing_speed", "State")
        self.shutdown_time = getValueDb(f"settings_{self.username}", "Service", "shutdown_time", "State")
        self.scroll_up = getValueDb(f"settings_{self.username}", "Service", "scroll_up", "State")
        self.scroll_down = getValueDb(f"settings_{self.username}", "Service", "scroll_down", "State")
        
        # Init the assistant
        self.read_text("Starting assistant", volumen=self.volumen_user, state=self.voice)
        self.beep(1200, 700, state=self.sound)
        while True:
            self.listen_commands()
    
    def voice_models(self):
        """
        Returns the available voices.
        """
        engine = pyttsx3.init()
        voices_models = engine.getProperty('voices')

        voices = []
        for voice in voices_models:
            voices.append(voice.name)
        print(voices)

    def execute_commands(self, command):
        """
        Executes commands given to the assistant.

        Args:
            command (str): The command to execute.
        """
        

        if "write" in command:
            print("Starting to write")
            texto_para_escribir = ""

            # Eliminate the text before the command "write"
            pos_write = command.find("write")
            command = command[pos_write:]

            command = command.replace("assistant", "")
            command = command.replace("write", "")
            command = command.strip()
            try:
                command = command[0].upper() + command[1:]
            except:
                pyautogui.alert('You must say "write {text you want to write}', title="And the text?")
            
            # Transform verbal language to written language
            command = command.replace(" comma", ", ")
            command = command.replace(" colon", ": ")
            command = command.replace(" semicolon", "; ")
            command = command.replace(" period", ". ")
            command = command.replace(" open question", "¿")
            command = command.replace(" close question", "?")
            command = command.replace(" open exclamation", "¡")
            command = command.replace(" close exclamation", "!")
            command = command.replace(" open parentheses", "(")
            command = command.replace(" close parentheses", ")")
            command = command.replace(" open brackets", "[")
            command = command.replace(" close brackets", "]")
            command = command.replace(" open brace", "{")
            command = command.replace(" close brace", "}")
            command = command.replace(' open quotes', '"')
            command = command.replace(' close quotes', '"')
            command = command.replace(" line break", ".\n")
            command = command.replace(" hashtag symbol", "#")
            command = command.replace(" dollar symbol", "$")
            command = command.replace(" euro symbol", "€")
            command = command.replace(" and symbol", "&")
            command = command.replace(" at symbol", "@")
            command = command.replace(" equal symbol", "=")
            command = command.replace(" slash symbol", "/")
            command = command.replace(" backslash symbol", "\\")
            command = command.replace(" plus symbol", "+")
            command = command.replace(" minus symbol", "-")
            command = command.replace(" asterisk symbol", "*")
            command = command.replace(" percentage symbol", "%")
            command = command.replace(" hyphen", "-")
            command = command.replace(" underscore", "_")
            command = command.replace(" space ", " ")
            
            # Write a period if the text ends without any symbol
            if command[0:-1] != "?" and command[0:-1] != "!" and command[0:-1] != "." and command[0:-1] != "," and command[0:-1] != ";":
                command = command + ". "
            
            texto_para_escribir = command
            keyboard.write(texto_para_escribir.strip(), delay=self.writing_speed)
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

        if "open chrome" in command.lower() or "open internet" in command.lower():
            print("Opening chrome...")
            self.read_text("Opening internet", volumen=self.volumen_user, state=self.voice)
            subprocess.run(["start","chrome"])
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

        if "open notepad" in command.lower():
            print("Opening notepad...")
            self.read_text("Opening notepad", volumen=self.volumen_user, state=self.voice)
            notepad_process = subprocess.Popen(["notepad.exe"])
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

        if "close chrome" in command or "close internet" in command.lower():
            self.read_text("Closing internet", volumen=self.volumen_user, state=self.voice)
            time.sleep(0.5)
            pyautogui.hotkey("alt","f4")
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

        if "close notepad" in command.lower():
            self.read_text("Closing notepad", volumen=self.volumen_user, state=self.voice)
            notepad_process.terminate()
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

        if "hello assistant" in command.lower():
            self.read_text("Hello, I'm the assistant created by Jose Antonio Sabio Prados. How can I help you?", volumen=self.volumen_user, state=self.voice)
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

        if "thank you assistant" in command.lower():
            self.read_text("You're welcome", volumen=self.volumen_user, state=self.voice)
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

        if "minimize window" in command.lower():
            time.sleep(0.5)
            self.minimize_window()
            self.read_text("Minimizing window", volumen=self.volumen_user, state=self.voice)
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

        if "maximize window" in command.lower():
            time.sleep(0.5)
            self.maximize_window()
            self.read_text("Maximizing window", volumen=self.volumen_user, state=self.voice)
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

        if "close window" in command.lower():
            time.sleep(0.5)
            pyautogui.hotkey("alt","f4")
            self.read_text("Closing window", volume=self.volumen_user, state=self.voice)
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

        if "disable assistant voice" in command.lower():
            self.read_text("Muting assistant", volume=self.volumen_user, state=self.voice)
            time.sleep(0.5)
            self.voice = False
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

        if "enable assistant voice" in command.lower():
            self.voice = True
            time.sleep(0.5)
            self.read_text("Reactivating voice", volume=self.volumen_user, state=self.voice)
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            self.beep(1200,800, state=self.sound)
            time.sleep(0.5)

        if "assistant search" in command.lower():
            print("Searching the internet...")
            self.read_text("Here are the search results", volume=self.volumen_user, state=self.voice)
            search_template = "https://www.google.com/search?q=z&oq=&aqs=chrome.0.69i59i450l8.434689207j0j15&sourceid=chrome&ie=UTF-8"
            text_to_search = ""
            command = command.replace("assistant","")
            command = command.replace("search","")
            text_to_search = command
            search = (text_to_search.strip()).replace(" ","+")
            search_url = search_template.replace("z", search)
            webbrowser.open(search_url)
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

        if "assistant open new window" in command.lower():
            pyautogui.hotkey("ctrl","n")
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

        if "assistant close window" in command.lower():
            pyautogui.hotkey("alt","f4")
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

        if "assistant open new tab" in command.lower():
            pyautogui.hotkey("ctrl","t")
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

        if "assistant close tab" in command.lower():
            pyautogui.hotkey("ctrl","w")
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

        if "assistant which is the volume" in command.lower() or "volume of assistant" in command.lower():
            vol_read = int(self.volumen_user * 100)
            msg_vol = "My volume is "+str(vol_read)+" percent. To change it say, assistant change volume to, plus the number from 1 to 10"
            self.read_text(msg_vol, volume=self.volumen_user, state=self.voice)
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

        if "assistant change volume to" in command.lower():
            # Find the number in the command
            words = command.split()
            for word in words:
                if word.lower() in self.list_numbers:
                    # Convert word to number
                    vol_num = int(self.list_numbers.index(word.lower())+1)
                    print(vol_num)
                    self.volumen_user = float(float(vol_num) / 10.0)  # Adjust volume to a value between 0.1 and 1.0
                    print(f"Changing volume to {vol_num}")
                    self.read_text(f"Changing volume to {vol_num*10} percent", volume=self.volumen_user, state=self.voice)
                    self.beep(300,300, state=self.sound)
                    self.beep(650,300, state=self.sound)
                    time.sleep(0.5)
                    break 

        if "open file" in command.lower():
            # Open a file of any extension
            
            # Get the file and its extension from the user's input voice (command variable)
            command = command.replace("open file", "").strip()
            command = command.replace("dot", ".")
            command = command.replace(" ", "")
            
            # Get the path of the current user's home directory
            user_directory_path = os.path.expanduser("~")

            # Build the full file path
            file_location = os.path.join(user_directory_path, "Desktop\\", command)
            
            if os.path.exists(file_location):
                os.startfile(file_location)
                self.read_text("Opening file "+command, volume=self.volumen_user, state=self.voice)
                self.beep(1700,900, state=self.sound)
                self.beep(400,500, state=self.sound)
            else:
                self.read_text("The file does not exist", volume=self.volumen_user, state=self.voice)
                self.beep(1800,900, state=self.sound)
                self.beep(400,500, state=self.sound)

        if "go to home screen" in command.lower():
            # Press the Windows key to go to the start menu
            pyautogui.press("win")
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

        if "shutdown my computer" in command.lower():
            # Turn off the PC after a set time
            subprocess.run(['shutdown', '/s', '/t', self.shutdown_time], shell=True)
            self.read_text(f"The device will shut down in {self.shutdown_time} seconds. To cancel, say, cancel shutdown", volume=self.volumen_user, state=self.voice)
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            self.beep(1200,700, state=self.sound)
            self.beep(300,400, state=self.sound)

        if "cancel shutdown" in command.lower():
            # Cancel the shutdown
            subprocess.run(['shutdown', '/a'], shell=True)
            self.read_text("Shutdown canceled", volume=self.volumen_user, state=self.voice)
            self.beep(1800,900, state=self.sound)
            self.beep(400,500, state=self.sound)

        if "activate sound" in command.lower():
            # Activate sounds
            self.sound = True
            time.sleep(0.5)
            self.read_text("Sound activated", volume=self.volumen_user, state=self.voice)
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)

        if "desactivate sound" in command.lower():
            # Deactivate sounds
            self.sound = False
            self.read_text("Sound deactivated", volume=self.volumen_user, state=self.voice)

            ###############################################
        if "say the time" in command.lower():
            time.sleep(0.5)
            now = datetime.now()
            time = now.strftime("%H:%M")
            self.read_text(f"It's {time} now", volumen=self.volumen_user, state=self.voice)
            time.sleep(0.5)

        if "scroll up" in command.lower():
            time.sleep(0.5)
            pyautogui.scroll(self.scroll_up)
            self.read_text("Scrolling up", volumen=self.volumen_user, state=self.voice)
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

        if "scroll down" in command.lower():
            time.sleep(0.5)
            pyautogui.scroll(self.scroll_down)
            self.read_text("Scrolling down", volumen=self.volumen_user, state=self.voice)
            self.beep(300,300, state=self.sound)
            self.beep(650,300, state=self.sound)
            time.sleep(0.5)

    def beep(self, frequency, duration, state=True):
        """
        Emits a self.sound if state is True.

        Args:
            frequency (int): The frequency of the beep self.sound.
            duration (int): The duration of the beep self.sound.
            state (bool): The state to check if the beep should occur.
        """
        if state:
            winsound.Beep(frequency, duration)

    def read_text(self, text, volumen=1.0, state=True):
        """
        Reads out the text if state is True.

        Args:
            text (str): The text to be read out.
            volumen (float): The volume of the speech (default is 1.0).
            state (bool): The state to check if the text should be read.
        """
        if state:
            engine = pyttsx3.init()
            engine.setProperty('volume', volumen)
            self.voices = self.voice_models()
            engine.setProperty('self.voice', self.voices[0].id)
            engine.say(text)
            engine.runAndWait()

    def minimize_window(self):
        """
        Minimizes the active window.
        """
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    def maximize_window(self):
        """
        Maximizes the active window.
        """
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    def listen_commands(self):
        """
        Listens to user commands using the microphone.
        """
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

            try:
                command = self.recognizer.recognize_google(audio, language='en-US').lower()
                print(f"User said: {command}")
                self.execute_commands(command)

            except sr.UnknownValueError:
                print("Assistant could not understand the audio")
            
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service; check your internet connection")
                pyautogui.alert("Assistant could not understand the audio")

if __name__ == "__main__":
    h = Voice_Assistant("josesp07")
