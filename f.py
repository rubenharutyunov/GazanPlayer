# -*- coding: utf-8 -*-
import pygame,Tkinter, tkMessageBox,tkFileDialog, datetime, time, sys, threading, os, mad

root = Tkinter.Tk()
root.title("Gazan")
root.geometry('150x200')
root.iconbitmap("@icon.xbm")

fn = ""
paused = False
a = False

def exiter():
    choice = tkMessageBox.askokcancel(title="Quit", message="Are you sure?")
    if choice == True:
        root.destroy()
        return


def askFile():
    global fn
    fn =  tkFileDialog.askopenfile(parent=root)
    print fn
    run_play_in_new_thread(fn)
 

def play(song):
    pygame.mixer.init(44100, -16, 2, 2048) 
    pygame.mixer.music.load(song)
    mf = mad.MadFile(song)
    track_length_in_mseconds = mf.total_time() + 1
    if c1.get() == 0:
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.play(-1)
    while pygame.mixer.music.get_busy():
        if pygame.mixer.music.get_pos() <= track_length_in_mseconds:
            pos = pygame.mixer.music.get_pos()/ 1000       
        else:
            var =  track_length_in_mseconds - 20
            pos =  (pygame.mixer.music.get_pos() - var) / 1000
        a = '\r' + str(datetime.datetime.fromtimestamp(pos).strftime('%M:%S'))
        timelab.configure(text=a)
        time.sleep(1)


def play_pause():
    global paused
    paused = not paused
    print paused
    if paused: pygame.mixer.music.pause()
    else: pygame.mixer.music.unpause()


def run_play_in_new_thread(song):
    th = threading.Thread(target=play, args=(song,))
    th.daemon = True
    th.start()


c1 = Tkinter.IntVar()
PButton = Tkinter.Button(root, text="Pause/UnPause", command = play_pause).pack()
FButton = Tkinter.Button(root, text="Choose file", command = askFile).pack()
PlayButton = Tkinter.Button(root, text="Play", command = run_play_in_new_thread).pack()
timelab = Tkinter.Label(root, text = 'start')
ExButton = Tkinter.Button(root, text="Exit", command = exiter).pack()
che1 = Tkinter.Checkbutton(root,text="Repeat",variable=c1,onvalue=1,offvalue=0).pack()
timelab = Tkinter.Label(root, text = 'start')
timelab.pack()
root.mainloop()
