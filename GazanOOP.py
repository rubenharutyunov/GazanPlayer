#!/usr/bin/python2
# -*- coding: utf-8 -*-
import pyglet
import time
import datetime
import sys, os
import datetime
import threading
import Tkinter  
import fileGrabber, PyQT
from mutagen import File
from PIL import ImageTk, Image# imports
from PySide import QtCore, QtGui


class GazanPlayer():

    def __init__(self):
        #self.play = []  # I don't need it, but let it be :-)
        self.player = pyglet.media.Player()  # Initlialize the player
        self.player.eos_action = self.player.EOS_NEXT # It's necessary if I want music to loop
        self.pos = 1
                
    def pause(self):  # Simple pause :-)
        self.player.pause()

    def unpause(self):  # Simple unpause :-)
        self.player.play()
        threading.Thread(target=self.hgh).start()

    def seek_five_secs(self):  # Simple seek, maybe I'll make it better
        self.player.seek(self.player.time+5)  # Seek to position

    def seek_minus_file_secs(self):  # Contrariwise
        self.player.seek(self.player.time-5)

    def next(self):
        self.player.next()    


class PlayThread(QtCore.QThread):
  def __init__(self, ex=None, files=[], parent=None):
    super(PlayThread, self).__init__(parent)
    self.test = ex
    self.files = files


  def __del__(self):
    self.wait()

  def playFile(self):
        for file in self.files:
            self.song = pyglet.media.load(file)  # Load the file
            self.test.player.queue(self.song)  # Put the file into a queue
            #self.play.append(self.song.info.title)
            try:
                fileMp3 = File(file)
                if file.endswith('.mp3'):
                    artwork = fileMp3.tags['APIC:'].data
                elif file.endswith('.m4a') or file.endswith('.mp4'): 
                    artwork = fileMp3.tags['covr'][0]
                elif file.endswith('.flac'):  
                    artwork =  fileMp3.pictures[0].data  
                else:
                    artwork =  ''
                if artwork and self.song.info.album:
                    with open('%s.jpg' % (self.song.info.album), 'wb') as img:
                         img.write(artwork) # write artwork to new image  
            except KeyError:
                pass          
                          

  def run(self):
    self.playFile()
    self.test.player.play() 
    

class ConfThread(QtCore.QThread):
    def __init__(self, ex=None, parent=None):
        super(ConfThread, self).__init__(parent)
        self.test = ex
        
    def __del__(self):
        self.wait()

    def conf(self):
        while self.test.player.playing:
            #print  "Current: " + " " + self.play[self.play.index(self.player.source.info.title)]
            title = [self.test.player.source.info.title,  "Unknown"][self.test.player.source.info.title == '']
            author = [self.test.player.source.info.author, "Unknown"][self.test.player.source.info.author == '']
            album =  [self.test.player.source.info.album, "Unknown"][self.test.player.source.info.album == '']
            genre = [self.test.player.source.info.genre, "Unknown"][self.test.player.source.info.genre == '']
            tg.labTitle.setText(title) 
            tg.labTitle.setToolTip(title)

            tg.labArtist.setText(author) 
            tg.labArtist.setToolTip(author)

            tg.labAlbum.setText(album) 
            tg.labAlbum.setToolTip(album)

            tg.labYear.setText(genre) 
            tg.labYear.setToolTip(album)

            a = '%s.jpg' % (self.test.player.source.info.album)
            tg.timer.display(str(datetime.datetime.fromtimestamp(test.player.time).strftime('%M:%S')))    
            time.sleep(1)  
            if os.path.isfile(a):
                self.emit(QtCore.SIGNAL("mysignal(QString)"), a)
            else:
                self.emit(QtCore.SIGNAL("mysignal(QString)"), 'logo.png')    

    def run(self):
        self.conf()
    

test = GazanPlayer()


class Gui(PyQT.PlayerGui):
    def __init__(self, parent=None):
        PyQT.PlayerGui.__init__(self, parent)
        self.th = ConfThread(ex=test)
        self.th2 = PlayThread(ex=test, files=fileGrabber.grabb_music_files())
        self.connect(self.butPlay, QtCore.SIGNAL("clicked()"), self.start)
        self.connect(self.th, QtCore.SIGNAL("mysignal(QString)"), self.on_change, QtCore.Qt.QueuedConnection)
        self.connect(self.th2, QtCore.SIGNAL("finished()"), self.on_finished)
        self.connect(self.butNext, QtCore.SIGNAL('clicked()'), test.next)
        

    def start(self):  
        print 'test'  
        self.th2.start(QtCore.QThread.Priority.TimeCriticalPriority)
        time.sleep(1)
        self.th.start()   

    def on_change(self, s):
        self.labArt.setFixedHeight(300)
        self.labArt.setFixedWidth(300)
        #print os.path.isfile(s), s
        self.labArt.setPixmap(QtGui.QPixmap(s))
        
        #self.labArt.setPixmap(QtGui.QPixmap('logo.png'))

    def on_finished(self):
        pass

app = QtGui.QApplication(sys.argv)
tg = Gui()
tg.show()
app.exec_()
