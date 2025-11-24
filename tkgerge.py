import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import tkinter as tk
from threading import Thread

opts = {
    "alias": ('Вася', 'Васена', 'Василек', 'Васятка', 'Васюня', 'Васюта', 'Васюша','Вася'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "radio": ('включи музыку', 'воспроизведи радио', 'включи радио'),
        "stupid1": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты')
    }
}

def speak(what):
    output_text.set(what)
    speak_engine.say(what)
    speak_engine.runAndWait()

def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU")
        output_text.set(f"Распознано: {voice}")
        
        if voice.startswith(opts["alias"]):
            cmd = voice
            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()
            
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])
    except sr.UnknownValueError:
        output_text.set("Голос не распознан!")
    except sr.RequestError:
        output_text.set("Ошибка! Проверьте интернет.")

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC

def execute_cmd(cmd):
    if cmd == 'ctime':
        now = datetime.datetime.now()
        speak(f"Сейчас {now.hour} {now.minute}")
    elif cmd == 'radio':
        os.system("C:\\Users\\User\\VoiceHelper\\res\\radio_record.m3u")
    elif cmd == 'stupid1':
        speak("Мой разработчик не научил меня анекдотам ... Ха ха ха ха")
    else:
        output_text.set('Команда не распознана, повторите!')

def start_listening():
    with m as source:
        r.adjust_for_ambient_noise(source)
    r.listen_in_background(m, callback)
    output_text.set("Вася слушает...")

def stop_program():
    root.destroy()

speak_engine = pyttsx3.init()
r = sr.Recognizer()
m = sr.Microphone(device_index=1)

root = tk.Tk()
root.title("Голосовой помощник Вася")
root.geometry("1280x720")

tk.Label(root, text="Голосовой помощник Вася", font=("Arial", 16)).pack(pady=10)
output_text = tk.StringVar()
tk.Label(root, textvariable=output_text, font=("Arial", 12)).pack(pady=20)

tk.Button(root, text="Начать слушать", command=lambda: Thread(target=start_listening).start()).pack(pady=10)
tk.Button(root, text="Выход", command=stop_program).pack(pady=10)

speak("Добрый день, повелитель")
speak("Вася слушает")

root.mainloop()
