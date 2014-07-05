#!/usr/bin/python
# -*- coding: utf-8 -*-
import pyglet
import time
import datetime
import sys
import datetime
import threading
import Tkinter  
import fileGrabber 
from mutagen import File
from PIL import ImageTk, Image# imports


class GazanPlayer():

    def __init__(self):
        self.play = False  # I don't need it, but let it be :-)
        self.player = pyglet.media.Player()  # Initlialize the player
        self.pos = 1
        pyglet.clock.schedule_interval(self.waitForExit, 1)

    # It's very important, without it player can't exit after playing!!!
    def waitForExit(self, dt):
        try:
            if self.player.playing:
                title = [self.player.source.info.title, "Unknown"][self.player.source.info.title == '']
                author = [self.player.source.info.author, "Unknown"][self.player.source.info.author == '']
                album =  [self.player.source.info.album, "Unknown"][self.player.source.info.album == '']
                genre = [self.player.source.info.genre, "Unknown"][self.player.source.info.genre == '']
                lab2.configure(text=author + ' '  + ' / ' + title + ' / ' + album + ' / ' + genre) 
                #print dir(self.player.source.info)
                a = '%s.jpg' % (self.player.source.info.album)
                original = Image.open(a)
                resized = original.resize((300, 300),Image.ANTIALIAS)
                img2 = ImageTk.PhotoImage(resized)
                labArt.configure(image=img2)
                time.sleep(5)
            else:
                labArt.configure(image=img20)
        except:
            labArt.configure(image=img20)   

        '''if not self.player.playing: 
            pyglet.app.exit()    # Exit!  ''' 
                
       
             
    def hgh(self):
        nt2()
        self.player.play()  # Start playing
        
            # Call waitForExit when song is over
        pyglet.app.run()  # Run!
        print "done!"   # Only for tests        


    def playFile(self, files):
        for file in files:
            self.song = pyglet.media.load(file)  # Load the file
            self.player.queue(self.song)  # Put the file into a queue
            self.player.eos_action = self.player.EOS_NEXT # It's necessary if I want music to loop
            fileMp3 = File(file)
            if file.endswith('.mp3'):
                artwork = fileMp3.tags['APIC:'].data
            elif file.endswith('.m4a') or file.endswith('.mp4'): 
                artwork = fileMp3.tags['covr'][0]
            elif file.endswith('.flac'):  
                artwork =  fileMp3.pictures[0].data  
            else:
                artwork =  ''
            
            with open('%s.jpg' % (self.song.info.album), 'wb') as img:
                 img.write(artwork) # write artwork to new image

   

        '''nt2()
        self.player.play()  # Start playing
        pyglet.clock.schedule_interval(self.waitForExit, 1)
            # Call waitForExit when song is over
        pyglet.app.run()  # Run!
        print "done!"   # Only for tests'''

        self.hgh()
        

    def pause(self):  # Simple pause :-)
        self.player.pause()

    def unpause(self):  # Simple unpause :-)
        self.player.play()
        threading.Thread(target=self.hgh).start()
        nt2()

    def seek_five_secs(self):  # Simple seek, maybe I'll make it better
        self.player.seek(self.player.time+5)  # Seek to position

    def seek_minus_file_secs(self):  # Contrariwise
        self.player.seek(self.player.time-5)

    def next(self):
        self.player.next()    



#----------------------Only-for-tests-I'll-use-PyQt-----------------------
test = GazanPlayer()


def timer():
    while test.player.playing:
        lab.configure(
            text=str(datetime.datetime.fromtimestamp(test.player.time).strftime('%M:%S')))
        time.sleep(1.0)


def nt():
    song = "06. Eatin.m4a"
    th = threading.Thread(target=test.playFile, args=(fileGrabber.grabb_music_files(),))
    th.daemon = True
    th.start()
    time.sleep(0.5)
    nt2()


def nt2():
    th2 = threading.Thread(target=timer)
    th2.start()
nt2()
root = Tkinter.Tk()
root.geometry('510x520')
but = Tkinter.Button(root, text="Play", command=nt).pack()
but2 = Tkinter.Button(root, text="Pause", command=test.pause).pack()
but3 = Tkinter.Button(root, text="Unpause", command=test.unpause).pack()
but4 = Tkinter.Button(
    root, text="+5 second", command=test.seek_five_secs).pack()
but5 = Tkinter.Button(
    root, text="-5 second", command=test.seek_minus_file_secs).pack()
but6=Tkinter.Button(root, text="next", command=test.next).pack()
lab = Tkinter.Label(root, text="")
lab.pack()
lab2 = Tkinter.Label(root, text="Information")
lab2.pack()
labArt = Tkinter.Label(root, text='album art')

img20 = ImageTk.PhotoImage(Image.open('logo.png'))
labArt.configure(image=img20)
labArt.pack()
root.mainloop()

# test.playFile("Intro.mp3")
test.pause()