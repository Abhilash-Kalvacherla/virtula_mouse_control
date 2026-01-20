import speech_recognition as sr
import pyttsx3
import webbrowser
import eel
import os
import subprocess
import platform
import datetime
import pyperclip

# -----------------------------
# Initialize pyttsx3
# -----------------------------
engine = pyttsx3.init()

# -----------------------------
# Cross-platform file opener
# -----------------------------
def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.call(["open", path])
    else:  # Linux
        subprocess.call(["xdg-open", path])

# -----------------------------
# Speak + send to frontend
# -----------------------------
def reply(audio):
    print("Proton:", audio)
    engine.say(audio)
    engine.runAndWait()
    try:
        eel.addAppMsg(audio)   # send to frontend
    except:
        pass  # frontend may not be running

# -----------------------------
# Choose microphone at startup
# -----------------------------
def choose_microphone():
    try:
        import pyaudio
    except Exception:
        print("PyAudio not available, listing all devices (may include outputs)...")
        mic_list = sr.Microphone.list_microphone_names()
        for i, mic_name in enumerate(mic_list):
            print(f"{i}: {mic_name}")

        while True:
            try:
                choice = int(input("Enter the index of the microphone you want to use: "))
                if 0 <= choice < len(mic_list):
                    print(f"Using microphone: {mic_list[choice]}")
                    return choice
                else:
                    print("Invalid index, try again.")
            except ValueError:
                print("Please enter a valid number.")

    p = pyaudio.PyAudio()
    input_devices = []
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info.get('maxInputChannels', 0) > 0:
            input_devices.append((i, info.get('name')))
    p.terminate()

    if not input_devices:
        print("No input-capable audio devices found. Check drivers or install PyAudio.")
        return None

    print("Available input devices:")
    for j, (idx, name) in enumerate(input_devices):
        print(f"{j}: {name} (device index {idx})")

    while True:
        try:
            choice = int(input("Enter the index of the microphone you want to use (left number): "))
            if 0 <= choice < len(input_devices):
                selected_idx = input_devices[choice][0]
                print(f"Using microphone: {input_devices[choice][1]} (device index {selected_idx})")
                return selected_idx
            else:
                print("Invalid index, try again.")
        except ValueError:
            print("Please enter a valid number.")

MIC_INDEX = choose_microphone()

# -----------------------------
# Listen to microphone
# -----------------------------
def record_audio():
    r = sr.Recognizer()
    try:
        with sr.Microphone(device_index=MIC_INDEX) as source:
            print("Adjusting for background noise... Please wait")
            r.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            audio = r.listen(source)
    except Exception as e:
        print("Audio device error:", e)
        reply("Audio device error. Please restart and choose a different microphone.")
        return ""

    try:
        voice_data = r.recognize_google(audio)
        print("You said:", voice_data)
        return voice_data.lower()
    except sr.UnknownValueError:
        reply("Sorry, I did not understand that")
    except sr.RequestError:
        reply("Speech recognition service is unavailable")
    return ""

# -----------------------------
# Respond to user commands
# -----------------------------
listening = True
gesture_process = None

def respond(voice_data):
    global listening, gesture_process
    voice_data = voice_data.replace("proton", "").strip().lower()

    app_commands = {
        "text editor": "gedit",
        "gedit": "gedit",
        "file manager": "nautilus",
        "files": "nautilus",
        "calculator": "gnome-calculator",
        "terminal": "gnome-terminal",
        "browser": "firefox",
        "firefox": "firefox",
        "chrome": "google-chrome",
        "vlc": "vlc",
        "libreoffice": "libreoffice",
        "settings": "gnome-control-center",
    }
    website_commands = {
        "youtube": "https://www.youtube.com",
        "gmail": "https://mail.google.com",
        "google": "https://www.google.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://twitter.com",
        "github": "https://github.com",
        "stackoverflow": "https://stackoverflow.com",
    }

    if not listening and "wake up" not in voice_data:
        reply("Proton is sleeping. Say 'wake up' to activate.")
        return

    if "launch gesture recognition" in voice_data:
        reply("Launching gesture recognition...")
        try:
            gesture_process = subprocess.Popen(["python3", "Gesture_Controller.py"])
        except Exception as e:
            reply(f"Could not launch gesture recognition. Error: {e}")

    elif "stop gesture recognition" in voice_data:
        reply("Stopping gesture recognition...")
        try:
            if gesture_process and gesture_process.poll() is None:
                gesture_process.terminate()
                reply("Gesture recognition stopped.")
            else:
                reply("Gesture recognition is not running.")
        except Exception as e:
            reply(f"Could not stop gesture recognition. Error: {e}")

    elif "search" in voice_data:
        query = voice_data.split("search", 1)[-1].strip()
        if query:
            reply("Searching for " + query)
            url = "https://google.com/search?q=" + query
            try:
                webbrowser.get().open(url)
                reply("This is what I found")
            except:
                reply("Please check your Internet connection")
        else:
            reply("Please tell me what to search")

    elif "location" in voice_data:
        location = voice_data.split("location", 1)[-1].strip()
        if location:
            reply("Showing location of " + location)
            url = "https://google.com/maps/place/" + location
            try:
                webbrowser.get().open(url)
                reply("Here you go")
            except:
                reply("Please check your Internet connection")
        else:
            reply("Please tell me which location to find")

    elif "open" in voice_data:
        app = voice_data.replace("open", "").strip()
        if app:
            if app in app_commands:
                reply(f"Opening {app}")
                try:
                    subprocess.Popen([app_commands[app]])
                except Exception as e:
                    reply(f"Could not open {app}. Error: {e}")
            elif app in website_commands:
                reply(f"Opening {app}")
                try:
                    webbrowser.get().open(website_commands[app])
                except Exception as e:
                    reply(f"Could not open {app}. Error: {e}")
            else:
                reply(f"Opening {app}")
                try:
                    open_file(app)
                except Exception as e:
                    reply(f"Could not open {app}. Error: {e}")
        else:
            reply("Please specify what to open")

    elif "date" in voice_data or "time" in voice_data:
        now = datetime.datetime.now()
        reply(f"The current date and time is {now.strftime('%Y-%m-%d %H:%M:%S')}")

    elif "copy" in voice_data:
        text = voice_data.replace("copy", "").strip()
        pyperclip.copy(text)
        reply("Copied to clipboard.")

    elif "paste" in voice_data:
        pasted = pyperclip.paste()
        reply(f"Pasted: {pasted}")

    elif "sleep" in voice_data:
        listening = False
        reply("Proton is now sleeping.")
    elif "wake up" in voice_data:
        listening = True
        reply("Proton is awake.")

    elif "exit" in voice_data or "quit" in voice_data:
        reply("Goodbye, Sir")
        try:
            eel.close()
        except:
            pass
        exit()

    else:
        reply("I did not understand, can you repeat?")

# -----------------------------
# Exposed to frontend  
# -----------------------------
@eel.expose
def getUserInput(msg):
    reply("You said: " + msg)
    respond(msg)

# -----------------------------
# MAIN FUNCTION
# -----------------------------
if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    web_folder = os.path.join(path, "web")
    eel.init(web_folder)

    eel.start("index.html", mode="chrome", port=27005, block=False, size=(400, 600))

    reply("Hello Sir, I am Proton. How can I help you?")

    while True:
        try:
            eel.sleep(1.0)
            voice_data = record_audio()
            if voice_data:
                respond(voice_data)
        except KeyboardInterrupt:
            reply("Shutting down...")
            break
        except Exception as e:
            print("Exception:", str(e))
            break