#!/usr/bin/python
# -*- coding: utf-8 -*-
import pyglet
import time
import datetime
import sys
import datetime
import threading
import Tkinter  # imports


class GazanPlayer():

    def __init__(self):
        self.play = False  # I don't need it, but let it be :-)
        self.player = pyglet.media.Player()  # Initlialize the player
        self.pos = 5

    # It's very important, without it player can't exit after playing!!!
    def waitForExit(self, dt):
        if not self.player.playing:  # It's not necessary now :-)
            pyglet.app.exit()    # Exit!

    def playFile(self, file):
        self.song = pyglet.media.load(file)  # Load the file
        self.player.queue(self.song)  # Put the file into a queue
        # self.player.eos_action = self.player.EOS_LOOP  # It's necessary if I want music to loop
        # print self.song.duration
        self.player.play()  # Start playing
        # Call waitForExit when song is over
        pyglet.clock.schedule_once(self.waitForExit, self.song.duration)
        pyglet.app.run()  # Run!
        print "done!"   # Only for tests

    def pause(self):  # Simple pause :-)
        self.player.pause()

    def unpause(self):  # Simple unpause :-)
        self.player.play()
        nt2()

    def seek_five_secs(self):  # Simple seek, maybe I'll make it better
        self.player.seek(self.pos)  # Seek to position
        self.pos += 5  # Position + 5
        print self.pos  # Only for tests

    def seek_minus_file_secs(self):  # Contrariwise
        self.player.seek(self.pos)
        self.pos -= 5  # Position - 5
        print self.pos


#----------------------Only-for-tests-I'll-use-PyQt-----------------------
test = GazanPlayer()


def timer():
    while test.player.playing:
        lab.configure(
            text=str(datetime.datetime.fromtimestamp(test.player.time).strftime('%M:%S')))
        time.sleep(1.1)


def nt():
    song = "06. Eatin.m4a"
    th = threading.Thread(target=test.playFile, args=(song,))
    th.daemon = True
    th.start()
    time.sleep(0.5)
    nt2()


def nt2():
    th2 = threading.Thread(target=timer)
    th2.start()
nt2()
root = Tkinter.Tk()
but = Tkinter.Button(root, text="Play", command=nt).pack()
but2 = Tkinter.Button(root, text="Pause", command=test.pause).pack()
but3 = Tkinter.Button(root, text="Unpause", command=test.unpause).pack()
but4 = Tkinter.Button(
    root, text="+5 second", command=test.seek_five_secs).pack()
but5 = Tkinter.Button(
    root, text="-5 second", command=test.seek_minus_file_secs).pack()
#but6=Tkinter.Button(root, text="-hh", command=nt2).pack()
lab = Tkinter.Label(root, text="")
lab.pack()
root.mainloop()

# test.playFile("Intro.mp3")
test.pause()
