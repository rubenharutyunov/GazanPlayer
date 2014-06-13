#!usr/bin/python
# -*- coding: utf-8 -*-
import pyglet 
import time, sys, datetime, threading, Tkinter # imports

class GazanPlayer():
    def __init__(self):
        self.play = False # I don't need it, but let it be :-)
        self.player = pyglet.media.Player() # Initlialize the player
        self.pos = 5

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
        print "done!"   # Only for tests

    def pause(self):  # Simple pause :-)
        self.player.pause()

    def unpause(self):  # Simple unpause :-)
        self.player.play()    

    def seek_five_secs(self):   # Simple seek, maybe I'll make it better 
        self.player.seek(self.pos)  # Seek to position
        self.pos+=5  # Position + 5
        print self.pos  # Only for tests
    
    def seek_minus_file_secs(self):  #Contrariwise 
        self.player.seek(self.pos)
        self.pos-=5  # Position - 5
        print self.pos     


#----------------------Only-for-tests-I'll-use-PyQt------------------------------


test = GazanPlayer()

def nt():
    song = "file.mp3"
    th = threading.Thread(target=test.playFile, args=(song,))
    th.daemon = True
    th.start()

root = Tkinter.Tk()
but=Tkinter.Button(root, text="Play", command=nt).pack()
but2=Tkinter.Button(root, text="Pause", command=test.pause).pack()
but3=Tkinter.Button(root, text="Unpause", command=test.unpause).pack()
but4=Tkinter.Button(root, text="+5 second", command=test.seek_five_secs).pack()
but5=Tkinter.Button(root, text="-5 second", command=test.seek_minus_file_secs).pack()
root.mainloop()

#test.playFile("Intro.mp3")
test.pause()