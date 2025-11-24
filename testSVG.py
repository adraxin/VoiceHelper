from tkinter import *
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
    global stop_listening_handle
    with m as source:
        r.adjust_for_ambient_noise(source)
    stop_listening_handle = r.listen_in_background(m, callback)
    output_text.set("Вася слушает...")

def stop_listening():
    if stop_listening_handle:
        stop_listening_handle()
        output_text.set("Прослушивание остановлено.")

def continue_listening():
    stop_listening()
    start_listening()

def stop_program():
    stop_listening()  # Остановить слушание перед выходом
    root.destroy()

speak_engine = pyttsx3.init()
r = sr.Recognizer()
m = sr.Microphone(device_index=1)



root = tk.Tk()
root.title("Голосовой помощник Вася")
root.geometry("800x600")

# Загрузка изображений для кнопок
stop_img = PhotoImage(file="button/pause.png").subsample(5, 5)
continue_img = PhotoImage(file="button/start.png").subsample(3, 3)
exit_img = PhotoImage(file="button/stop.png").subsample(5, 5)


tk.Label(root, text="Голосовой помощник Вася", font=("Arial", 16)).pack(pady=10)
output_text = tk.StringVar()
tk.Label(root, textvariable=output_text, font=("Arial", 12)).pack(pady=20)

frame = tk.Frame(root)
frame.pack(side="bottom", pady=20)  # Упаковка всех кнопок внизу окна

# Кнопка для прекращения слушания
tk.Button(frame, image=stop_img, command=stop_listening, borderwidth=0
).pack(side="left", padx=110)

# Кнопка для продолжения слушания
tk.Button(frame, image=continue_img, command=continue_listening,
    borderwidth=0
).pack(side="left", padx=10)

# Кнопка для выхода
tk.Button(
    frame, image=exit_img, command=stop_program,
    borderwidth=0
).pack(side="right", padx=110)

# Загрузка иконки для окна
window_icon = PhotoImage(file="svg/svg.png")
root.iconphoto(True, window_icon)

root.after(1000, lambda: speak("Добрый день, повелитель"))
root.after(2000, lambda: speak("Вася слушает..."))

# Автоматически начать слушать при запуске
start_listening()

root.mainloop()
