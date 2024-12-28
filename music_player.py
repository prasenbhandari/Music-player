import tkinter as tk
from tkinter import HORIZONTAL, Listbox, filedialog
from pygame import mixer, USEREVENT
import os
import json
from mutagen.mp3 import MP3
import pygame

config_file = "config.json"
path = ""
current_index = 0
total_songs = 0
user_seeking = False
actual_start_time = 0
song_path = ""
SONG_END = USEREVENT
mixer.music.set_endevent(SONG_END)

mixer.init()
pygame.init()

def check_song_end():
    global SONG_END
    for event in pygame.event.get():
        if event.type == SONG_END:
            play_next()

    root.after(100, check_song_end)


def update_song(song_path):
    song = MP3(song_path)
    artist = song.tags.get("TPE1", "Unknown Artist")
    print(artist)
    title = song.tags.get("TIT2", "Unknown Title")
    song_name = f"{artist} - {title}"
    name.config(text=song_name)
    total_length = song.info.length
    min, sec = get_time(total_length)
    song_length.config(text=f"{min:02}:{sec:02}")
    play_time.config(text="00:00")


def get_time(total_length):
    total_length = int(total_length)
    min = total_length // 60 
    sec = total_length % 60
    return min, sec


def play_song(index):
    global actual_start_time, song_path
    song_name = lb.get(index)
    song_path = os.path.join(path, song_name)
    song = MP3(song_path)
    progress_slider.config(from_=0, to=song.info.length)
    mixer.music.unload()
    mixer.music.load(song_path)
    mixer.music.play()
    actual_start_time = 0
    update_song(song_path)
    update_progress()
    mixer.music.set_endevent(SONG_END)
    check_song_end()


def play_selected(event):
    global current_index
    current_index = lb.curselection()[0]
    play_song(current_index)
    play_pause_btn.config(text="", command=pause_music)


def play_next():
    global current_index
    index = (current_index + 1) % total_songs
    current_index = index
    play_song(index)

def play_previous():
    if (mixer.music.get_pos() / 1000) < 10:
        global current_index
        index = (current_index - 1) % total_songs
        current_index = index
        play_song(index)
    else:
        mixer.music.set_pos(0)



def load_selected(event):
    # TODO
    song = lb.get(lb.curselection())
    mixer.music.unload()
    mixer.music.load(os.path.join(path, song))


def load_music_folder():
    folder_path = filedialog.askdirectory()
    with open(config_file, 'w') as file:
        json.dump({"folder_path": folder_path}, file)


def load_music_list(folder_path):
    global total_songs
    lb.delete(0, tk.END)
    total_songs = 0
    for index, filename in enumerate(os.listdir(folder_path)):
        if filename.endswith(".mp3"):
            total_songs += 1
            lb.insert(index, filename)


def pause_music():
    mixer.music.pause()
    update_button()


def resume_music():
    mixer.music.unpause()
    update_button()


def update_button():
    if mixer.music.get_busy():  
        play_pause_btn.config(text="", command=pause_music)
    else:  
        play_pause_btn.config(text="", command=resume_music)


def update_progress():
    global user_seeking
    if not user_seeking:
        if mixer.music.get_busy():
            current_time = actual_start_time + (mixer.music.get_pos() / 1000)
            progress_slider.set(current_time)
            min, sec = get_time(current_time)
            play_time.config(text=f"{min:02}:{sec:02}")
            #print("hello")

    root.after(1000, update_progress)


def seek(event):
    global user_seeking, actual_start_time
    mixer.music.set_endevent(0)
    user_seeking = False
    actual_start_time  = progress_slider.get()
    mixer.music.stop()
    mixer.music.play(start=actual_start_time)
    mixer.music.set_pos(actual_start_time)
    mixer.music.set_endevent(SONG_END)
    

def start_seeking(event):
    global user_seeking
    user_seeking = True
    mixer.music.pause()


root = tk.Tk()
root.title("Music Player")
root.rowconfigure(0, weight=2)
root.rowconfigure(1, weight=0)
root.columnconfigure(0, weight=1)
root.geometry("600x500")


list_frame = tk.Frame(root)
list_frame.grid(row=0, column=0, sticky="nsew")
list_frame.grid_rowconfigure(0, weight=1)
list_frame.grid_columnconfigure(0, weight=1)

lb = Listbox(list_frame, selectmode=tk.SINGLE)
lb.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", ipadx=10, ipady=10)

operations_frame = tk.Frame(root)
operations_frame.grid(row=2, column=0)
operations_frame.grid_columnconfigure(0, weight=0)  
operations_frame.grid_columnconfigure(1, weight=0)  
operations_frame.grid_columnconfigure(2, weight=0)

play_pause_btn = tk.Button(operations_frame, text="", command=resume_music)
play_pause_btn.grid(row=0, column=1, padx=10, pady=10)
next_btn = tk.Button(operations_frame, text="󰒭", command=play_next)
next_btn.grid(row=0, column=2, padx=10, pady=10)
previous_btn = tk.Button(operations_frame, text="󰒮", command=play_previous)
previous_btn.grid(row=0, column=0, padx=10, pady=10)

progress_frame = tk.Frame(root)
progress_frame.grid(row=1)

name = tk.Label(progress_frame, text="No Song Playing")
name.grid(row=0, columnspan=3)
progress_slider = tk.Scale(progress_frame,from_=0, orient=HORIZONTAL, length=500)
progress_slider.grid(row=1, column=1, padx=10)
play_time = tk.Label(progress_frame,text="00:00")
play_time.grid(row=1, column=0)
song_length = tk.Label(progress_frame,text="00:00")
song_length.grid(row=1, column=2, padx=10)

if os.path.exists(config_file):
    with open(config_file, 'r') as file:
        data = json.load(file)
        path = data.get("folder_path","")
        load_music_list(path)
else:
    load = tk.Button(root, text="Load Music Folder", command=load_music_folder)
    load.place(relx=0.5, rely=0.5, anchor="center")


lb.bind("<Double-1>", play_selected)
#lb.bind("<Button-1>", load_selected)
progress_slider.bind("<ButtonRelease-1>", seek)
progress_slider.bind("<ButtonPress-1>", start_seeking)


root.mainloop()


