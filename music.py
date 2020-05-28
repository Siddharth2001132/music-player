# python modules
from tkinter import messagebox
from pygame import mixer
import tkinter as tkr
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
import os
import pygame
from PIL import Image, ImageTk
from itertools import count
import datetime
from mutagen.mp3 import MP3
# import required libraries
from vidgear.gears import CamGear
import cv2

#########################################################################
global file, play_list, play_button, pause_button, volume_value, value, music_len, plus, \
    ProgressBarMusic, ProgressBarMusicEndTime, CurrentSongLength, ProgressBarMusicStartTime, Song, \
    search_entry_label, search_list
song_list = []
song_path = []
song_history = []
search_song = []
pos = 0
play_button_click = False
paused = False
plus = False
mixer.init()


class ImageLabel(tkr.Label):
    """a label that displays images, and plays them if they are gifs"""

    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


def about_us():
    messagebox.showinfo('About us', "This is a music player created by Siddharth Rathod")


def browse_file():
    global play_button_click, play_list, file
    play_button_click = True
    file = filedialog.askdirectory(title='Select Folder')
    os.chdir(file)
    for i in os.listdir(file):
        if i.endswith(".mp3") or i.endswith(".mp4"):
            song_list.append(i)
            song_path.append(file + f'/{i}')
        song_list.reverse()

        play_list = tkr.Listbox(middle_frame, bg='#3b5998', width=90, font=('comic sans ms', 10), height=15,
                                yscrollcommand=True)
        play_list.grid(row=1, column=5, rowspan=2, columnspan=2, padx=(0, 20), pady=(0, 20))
        play_list.bind('<Double-1>', lambda a: Playnew())
        for song in song_list:
            play_list.insert(0, song)
        song_list.reverse()

        play_list.select_set(0, 0)
    print(song_list)
    print(song_path)


def Playnew():
    global paused
    paused = False
    Play()


def Play():
    global pos, play_button_click, play_button, pause_button, paused, song_history, song_list, plus, \
        ProgressBarMusic, ProgressBarMusicEndTime, CurrentSongLength, ProgressBarMusicStartTime, Song
    if not paused:
        if play_button_click:
            root.play_button.grid_remove()
            root.pause_button.grid()
            current_song = play_list.curselection()
            if not plus:
                pos = current_song[0]
            else:
                play_list.selection_clear(0, END)
                play_list.select_set(pos, pos)
                plus = False

            path = song_path[pos]
            mixer.music.load(path)
            pygame.mixer.music.play()
            song_history.append(song_list[pos])
            Song = MP3(path)
            total_song_length = int(Song.info.length)
            ProgressBarMusic['maximum'] = total_song_length
            ProgressBarMusicEndTime.configure(text=f'{str(datetime.timedelta(seconds=total_song_length))}')

            def Progressbarmusictick():
                CurrentSongLength = mixer.music.get_pos() // 1000
                ProgressBarMusic['value'] = CurrentSongLength
                ProgressBarMusicStartTime.configure(text=f'{str(datetime.timedelta(seconds=CurrentSongLength))}')
                ProgressBarMusic.after(2, Progressbarmusictick)

            Progressbarmusictick()
        else:
            tkr.messagebox.showerror("Empty List", "Empty Play List")
    else:
        root.play_button.grid_remove()
        root.pause_button.grid()
        pygame.mixer.music.unpause()
        paused = False


def Pause():
    global paused, play_button_click
    root.pause_button.grid_remove()
    root.play_button.grid()
    paused = True
    print(paused)
    mixer.music.pause()


def forward_func():
    global music_len, pos, plus
    try:
        pos += 1
        plus = True
        Play()
    except IndexError:
        pos = 0
        plus = True
        Play()


def backward_func():
    global plus, pos, music_len
    music_len = len(song_list)
    if pos == 0:
        try:
            pos = music_len - 1
            plus = True
            Play()
        except IndexError:
            pos = music_len - 1
            plus = True
            Play()
    else:
        try:
            pos -= 1
            plus = True
            Play()
        except IndexError:
            pos = music_len - 1
            plus = True
            Play()


def set_vol(val):
    global volume_value, value
    value = int(val)
    if value == 0:
        root.volume_button.grid_remove()
        root.volume_button = Button(bottom_frame, text='Play', font=('comic sans ms', 15),
                                    image=VOLUME_ZERO_IMG, relief="flat", activebackground='white', command=volume_func)
        root.volume_button.grid(row=0, column=4, padx=(20, 00), pady=20)
    elif 0 < value < 30:
        root.volume_button.grid_remove()
        root.volume_button = Button(bottom_frame, text='Play', font=('comic sans ms', 15),
                                    image=VOLUME2_IMG, relief="flat", activebackground='white', command=volume_func)
        root.volume_button.grid(row=0, column=4, padx=(20, 00), pady=20)
    elif 30 < value < 65:
        root.volume_button.grid_remove()
        root.volume_button = Button(bottom_frame, text='Play', font=('comic sans ms', 15),
                                    image=VOLUME3_IMG, relief="flat", activebackground='white', command=volume_func)
        root.volume_button.grid(row=0, column=4, padx=(20, 00), pady=20)
    else:
        root.volume_button.grid_remove()
        root.volume_button = Button(bottom_frame, text='Play', font=('comic sans ms', 15),
                                    image=VOLUME4_IMG, relief="flat", activebackground='white', command=volume_func)
        root.volume_button.grid(row=0, column=4, padx=(20, 00), pady=20)

    volume_value = int(val) / 100
    pygame.mixer.music.set_volume(volume_value)


def set_vol_same():
    global volume_value
    pygame.mixer.music.set_volume(volume_value)
    root.volume_mute_button.grid_remove()
    root.volume_button.grid()


def volume_func():
    pygame.mixer.music.set_volume(0)
    root.volume_button.grid_remove()
    root.volume_mute_button.grid()


def Stop():
    mixer.music.stop()


def history():
    if play_button_click and song_history:
        print(song_history)
        history_window = tkr.Toplevel(root)
        history_window.title("History")
        root.geometry("1380x680+10+200")
        history_window.geometry("500x700+1400+200")
        history_window.resizable(0, 0)
        history_list = tkr.Listbox(history_window, bg='#e9ebee', width=70, font=('comic sans ms', 10), height=100,
                                   yscrollcommand=True, xscrollcommand=True, relief='flat')
        history_list.grid(row=1, column=5, rowspan=2, columnspan=2, padx=(0, 20), pady=(0, 20))
        for song in song_history:
            history_list.insert(0, song)
    else:
        tkr.messagebox.showerror("History", "There's no History")


def Search():
    global search_entry_label, search_song, search_list
    search_window = tkr.Toplevel(root)
    search_window.title("Search")
    root.geometry("1380x680+10+200")
    search_window.geometry("500x100+710+65")
    search_window.resizable(0, 0)
    search_list = tkr.Listbox(search_window, bg='#e9ebee', width=70, font=('comic sans ms', 10), height=100,
                              yscrollcommand=True, xscrollcommand=True, relief='flat')
    search_list.grid(row=0, column=0, rowspan=2, columnspan=2, padx=(0, 20), pady=(0, 20))
    search_song_text = search_entry_label.get()
    for i in song_list:
        if search_song_text.lower() in i.lower():
            search_song.append(i)
    for i in search_song:
        search_list.insert(END, i)
    search_list.select_set(0, 0)

    def search_song_Play():
        global search_list, pos
        current_song = search_list.curselection()
        pos = current_song[0]
        path = search_song[pos]
        mixer.music.load(path)
        pygame.mixer.music.play()
        song_history.append(search_song[pos])

    search_list.bind('<Double-1>', lambda a: search_song_Play())


def visual_func():
    global ProgressBarMusic, ProgressBarMusicEndTime, CurrentSongLength, ProgressBarMusicStartTime, search_entry_label
    search_label = Label(top_frame, text="Search", background='#f7f7f7', font=('comic sans ms', 15))  # search
    search_label.grid(row=0, column=0, padx=(40, 0), pady=20)
    search_entry_label = tkr.Entry(top_frame, font=('comic sans ms', 15), width=85)
    search_entry_label.grid(row=0, column=1, padx=5, pady=20)
    search_button = Button(top_frame, text='Search', bg='#8b9dc3', font=('comic sans ms', 15), command=Search)
    search_button.grid(row=0, column=2, padx=(20, 20), pady=20)

    film_label = ImageLabel(middle_frame)
    film_label.grid(row=1, column=0, columnspan=5, pady=20, padx=40)
    film_label.load('assets/images/giphy.gif')

    back_button = Button(middle_frame, text='Play', bg='#3b5998', font=('comic sans ms', 15), image=BACKWARD_IMG,
                         relief="flat", activebackground='#3b5998', command=backward_func)
    back_button.grid(row=2, column=0, padx=(20, 20), pady=20)
    root.play_button = Button(middle_frame, text='Play', bg='#3b5998', font=('comic sans ms', 15), image=PLAY_IMG,
                              relief="flat", activebackground='#3b5998', command=Play)
    root.play_button.grid(row=2, column=1, padx=(20, 20), pady=20)
    root.pause_button = Button(middle_frame, text='Play', bg='#3b5998', font=('comic sans ms', 15), image=PAUSE_IMG,
                               relief="flat", activebackground='#3b5998', command=Pause)
    root.pause_button.grid(row=2, column=1, padx=(20, 20), pady=20)
    root.pause_button.grid_remove()

    stop_button = Button(middle_frame, text='Play', bg='#3b5998', font=('comic sans ms', 15), image=STOP_IMG,
                         relief="flat", activebackground='#3b5998', command=Stop)
    stop_button.grid(row=2, column=3, padx=(20, 20), pady=20)

    forward_button = Button(middle_frame, text='Play', bg='#3b5998', font=('comic sans ms', 15), image=FORWARD_IMG,
                            relief="flat", activebackground='#3b5998', command=forward_func)
    forward_button.grid(row=2, column=2, padx=(20, 20), pady=20)

    # ProgressBar
    ProgressBarMusicStartTime = tkr.Label(bottom_frame, text='0:00:0', bg='#9cb4d8')
    ProgressBarMusicStartTime.grid(row=0, column=1, padx=(20, 00), pady=20)

    ProgressBarMusic = Progressbar(bottom_frame, orient=HORIZONTAL, mode='determinate', value=0, length=470)
    ProgressBarMusic.grid(row=0, column=2, padx=(10, 00), pady=20)

    ProgressBarMusicEndTime = tkr.Label(bottom_frame, text='0:00:0', bg='#9cb4d8')
    ProgressBarMusicEndTime.grid(row=0, column=3, padx=(10, 00), pady=20)

    root.volume_button = Button(bottom_frame, text='Play', font=('comic sans ms', 15),
                                image=VOLUME2_IMG, relief="flat", activebackground='white', command=volume_func)
    root.volume_button.grid(row=0, column=4, padx=(20, 00), pady=20)

    root.volume_mute_button = Button(bottom_frame, text='Play', font=('comic sans ms', 15),
                                     image=VOLUME_MUTE_IMG, relief="flat", activebackground='white',
                                     command=set_vol_same)
    root.volume_mute_button.grid(row=0, column=4, padx=(20, 2), pady=20)
    root.volume_mute_button.grid_remove()

    volume_control = tkr.Scale(bottom_frame, from_=0, to=100, orient=HORIZONTAL, length=200, command=set_vol,
                               bg='#e9ebee', bd="0", highlightbackground="#e9ebee", highlightcolor="#3e5c9a",
                               troughcolor="#9cb4d8", activebackground="#3e5c9a", relief='flat')
    volume_control.set(32)
    mixer.music.set_volume(0.32)
    volume_control.grid(row=0, column=5, padx=(0, 20), pady=20)


#########################################################################

#########################################################################
# Create main window
root = tkr.Tk()
# Window
root.title("Music player")
root.iconbitmap("assets/images/music.ico")
root.geometry("1380x700+200+200")
root.resizable(0, 0)
root.configure(bg='#f7f7f7')

# Menubar
menubar = Menu(root)
root.config(menu=menubar)
# Sub menu
sub_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=sub_menu)
sub_menu.add_command(label='Open', command=browse_file)
sub_menu.add_command(label='History', command=history)
sub_menu.add_command(label='Exit')

sub_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=sub_menu)
sub_menu.add_command(label='About us', command=about_us)

# Frames
top_frame = tkr.Frame(root, bg='#f7f7f7', height='150')
top_frame.grid(row=0)

middle_frame = tkr.Frame(root, bg='#3b5998', height='150')
middle_frame.grid(row=1, padx=25)

bottom_frame = tkr.Frame(root)
bottom_frame.grid(row=2)
#########################################################################
#########################################################################
# Control button images
Img_width, Img_height = 50, 50
play = Image.open("assets/images/play.png")  # play
PLAY = play.resize((60, 60), Image.ANTIALIAS)
PLAY_IMG = ImageTk.PhotoImage(PLAY)
pause = Image.open("assets/images/pause.png")  # pause
PAUSE = pause.resize((60, 60), Image.ANTIALIAS)
PAUSE_IMG = ImageTk.PhotoImage(PAUSE)
stop = Image.open("assets/images/stop.png")  # stop
STOP = stop.resize((Img_width, Img_height), Image.ANTIALIAS)
STOP_IMG = ImageTk.PhotoImage(STOP)
forward = Image.open("assets/images/forward.png")  # forward
FORWARD = forward.resize((Img_width, Img_height), Image.ANTIALIAS)
FORWARD_IMG = ImageTk.PhotoImage(FORWARD)
backward = Image.open("assets/images/backward.png")  # forward
BACKWARD = backward.resize((Img_width, Img_height), Image.ANTIALIAS)
BACKWARD_IMG = ImageTk.PhotoImage(BACKWARD)
volume_zero = Image.open("assets/images/volume1.png")  # Volume up
VOLUME_ZERO = volume_zero.resize((Img_width, Img_height), Image.ANTIALIAS)
VOLUME_ZERO_IMG = ImageTk.PhotoImage(VOLUME_ZERO)
volume2 = Image.open("assets/images/volume2.png")  # Volume up
VOLUME2 = volume2.resize((Img_width, Img_height), Image.ANTIALIAS)
VOLUME2_IMG = ImageTk.PhotoImage(VOLUME2)
volume3 = Image.open("assets/images/volume3.png")  # Volume up
VOLUME3 = volume3.resize((Img_width, Img_height), Image.ANTIALIAS)
VOLUME3_IMG = ImageTk.PhotoImage(VOLUME3)
volume4 = Image.open("assets/images/volume4.png")  # Volume up
VOLUME4 = volume4.resize((Img_width, Img_height), Image.ANTIALIAS)
VOLUME4_IMG = ImageTk.PhotoImage(VOLUME4)
volume_mute = Image.open("assets/images/volume_mute.png")  # volume down
VOLUME_MUTE = volume_mute.resize((Img_width, Img_height), Image.ANTIALIAS)
VOLUME_MUTE_IMG = ImageTk.PhotoImage(VOLUME_MUTE)
world = Image.open("assets/images/worldwide.png")  # volume down
WORLD = world.resize((Img_width, Img_height), Image.ANTIALIAS)
WORLD_IMG = ImageTk.PhotoImage(WORLD)
connect = Image.open("assets/images/connect.png")  # volume down
CONNECT = connect.resize((Img_width, Img_height), Image.ANTIALIAS)
CONNECT_IMG = ImageTk.PhotoImage(CONNECT)
#########################################################################
#########################################################################
visual_func()
#########################################################################
# Main loop
root.mainloop()
