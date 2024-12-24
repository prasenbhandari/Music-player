import tkinter as tk
from tkinter import Listbox, filedialog
from pygame import mixer
import os
import json

config_file = "config.json"
path = ""
mixer.init()

def play_selected(event):
    song = lb.get(lb.curselection())
    mixer.music.load(os.path.join(path, song))
    mixer.music.play()

def load_music_folder():
    folder_path = filedialog.askdirectory()
    with open(config_file, 'w') as file:
        json.dump({"folder_path": folder_path}, file)

root = tk.Tk()

root.title("Music Player")

if os.path.exists(config_file):
    with open(config_file, 'r') as file:
        data = json.load(file)
        path = data.get("folder_path","")
else:
    load = tk.Button(root, text="Load Music Folder", command=load_music_folder)
    load.place(relx=0.5, rely=0.5, anchor="center")

lb = Listbox(root, selectmode=tk.SINGLE)

for index, filename in enumerate(os.listdir(path)):
    lb.insert(index, filename)

lb.bind("<Double-1>", play_selected)

lb.pack()

root.mainloop()
