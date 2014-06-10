#!usr/bin/python
# -*- coding: utf-8 -*-
import pyglet 
import time, sys, datetime, threading, Tkinter # imports

class GazanPlayer():
    def __init__(self):
        self.play = False # I don't need it, but let it be :-)
        self.player = pyglet.media.Player() # Initlialize the player

    def waitForExit(self,dt):  # It's very important, without it player can't exit after playing!!!
        if not self.player.playing: # It's not necessary now :-)
            pyglet.app.exit()    # Exit!
    
    def playFile(self, file):
        self.song = pyglet.media.load(file)  # Load the file
        self.player.queue(self.song)  # Put the file into a queue
        #self.player.eos_action = self.player.EOS_LOOP  # It's necessary if I want music to loop 
        #print self.song.duration
        self.player.play()  # Start playing
        pyglet.clock.schedule_once(self.waitForExit,self.song.duration) # Call waitForExit when song is over
        pyglet.app.run()  # Run!
        #print "done!"   # Only for tests

    def pause(self):  # Simplae pause :-)
        self.player.pause()


#----------------------Only-for-tests-I'll-use-PyQt------------------------------


test = GazanPlayer()

def nt():
    song = "Intro.mp3"
    th = threading.Thread(target=test.playFile, args=(song,))
    th.daemon = True
    th.start()

def ddd():
    test.player.pause()

root = Tkinter.Tk()
but=Tkinter.Button(root, text="gfgfg", command=nt).pack()
but2=Tkinter.Button(root, text="pause", command=ddd).pack()
root.mainloop()

#test.playFile("Intro.mp3")
test.pause()