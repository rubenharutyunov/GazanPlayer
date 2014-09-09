#!/usr/bin/python2
# -*- coding: utf-8 -*-
import pyglet
import time
import datetime
import sys, os
import datetime
import threading
import fileGrabber, PyQT
from db import DBConnect
from mutagen import File
from PIL import ImageTk, Image# imports
from PySide import QtCore, QtGui

reload(sys) # Reload sys to set
sys.setdefaultencoding('utf-8') # the default encoding

class GazanPlayer():
    '''
    This is a player class. This class simply initializes player and
    creates methods for playing/pausing and for getting the next track
    '''

    def __init__(self):
        self.play_files = []  # List of track titles
        self.player = pyglet.media.Player()  # Initialize the player
        self.player.eos_action = self.player.EOS_NEXT # It's necessary if I want to play next track from queue
                
    def pause(self):  # Simple pause :-)
        self.player.pause()

    def play(self):  # Simple play :-)
        self.player.play()

    def next(self):  # Next :-)
        self.player.next()    


class PlayThread(QtCore.QThread):
    '''
    This is a play thread. This thread loads and and plays music files from "files" argument. 
    Also, this thread creates cover images from music files
    '''

    def __init__(self, ex=None, files=[], parent=None):
        super(PlayThread, self).__init__(parent)
        self.instance = ex
        self.files = files

    def loadFiles(self):
        '''
        This method loads files, put them into queue, add the title of the track to "play" list(for displaying in the table)
        Also creates grabb artwork images and save them in file 
            TODO: program should save images in sqlite database, not files.
        '''
        untitled_count = 0 # Count of intitled songs (for list)
        for file in self.files:
            self.song = pyglet.media.load(file)  # Load the file
            self.instance.player.queue(self.song)  # Put the file into a queue
            #self.instance.player.volume = 0.1
            #if self.song.info.title not in self.instance.play_files:
            if not self.song.info.title: self.song.info.title =('Unknown%d' % untitled_count if untitled_count else 'Unknown'); untitled_count+=1 
            self.instance.play_files.append(self.song.info.title)  # add song to list
            try:
                fileMp3 = File(file)   # get artwork 
                if file.endswith('.mp3'):
                    artwork = fileMp3.tags['APIC:'].data
                elif file.endswith('.m4a') or file.endswith('.mp4'): 
                    artwork = fileMp3.tags['covr'][0]
                elif file.endswith('.flac'):  
                    artwork =  fileMp3.pictures[0].data  
                else:
                    artwork =  ''
                if artwork and self.song.info.album:
                    database = DBConnect('GPlayer.db')
                    database.add_image(self.song.info.album, artwork)
                    #with open('%s.jpg' % (self.song.info.album), 'wb') as img:
                         #img.write(artwork) # write artwork to new image  
            except (KeyError, TypeError) as e:
                pass          
                          

    def run(self):
        self.loadFiles()
        self.instance.player.play() 
    

class ConfThread(QtCore.QThread):
    '''
    This thread shows changes in GUI and sends signals to the main thread to show artworks.
    Argument ex shuld be instance of GazanPlayer class. 
    '''

    def __init__(self, ex=None, parent=None):
        super(ConfThread, self).__init__(parent)
        self.instance = ex
        
    def __del__(self):
        self.wait()

    def conf(self):
        while True:
            if self.instance.player.playing:
                # Info or "unknown"
                title = [self.instance.player.source.info.title,"Unknown"][self.instance.player.source.info.title.startswith('Unknown')]  
                author = [self.instance.player.source.info.author, "Unknown"][self.instance.player.source.info.author == '']
                album =  [self.instance.player.source.info.album, "Unknown"][self.instance.player.source.info.album == '']
                genre = [self.instance.player.source.info.genre, "Unknown"][self.instance.player.source.info.genre == '']
                
                # Set labels
                gui.labTitle.setText(unicode(title))
                gui.labTitle.setToolTip(unicode(title))

                gui.labArtist.setText(unicode(author)) 
                gui.labArtist.setToolTip(unicode(author))

                gui.labAlbum.setText(unicode(album)) 
                gui.labAlbum.setToolTip(unicode(album))

                gui.labYear.setText(unicode(genre)) 
                gui.labYear.setToolTip(unicode(genre))

                # Display time
                gui.timer.display(str(datetime.datetime.fromtimestamp(self.instance.player.time).strftime('%M:%S'))) 

                # Send signal every second   
                time.sleep(1)  
                a =  self.instance.player.source.info.album
                self.emit(QtCore.SIGNAL("mysignal(QString, QStringList)"), a, self.instance.play_files)
            else:  
                time.sleep(1)    # Sleep to not to use CPU!    

    def run(self):
        self.conf()
    

instance = GazanPlayer()


class Gui(PyQT.PlayerGui):
    '''
    This class extends base GUI class and binds GUI to player.
    '''

    def __init__(self, parent=None):
        PyQT.PlayerGui.__init__(self, parent,)
        self.th = ConfThread(ex=instance)
        self.connect(self.butPlay, QtCore.SIGNAL("clicked()"), self.start)
        self.connect(self.th, QtCore.SIGNAL("mysignal(QString, QStringList)"), self.on_change, QtCore.Qt.QueuedConnection)
        #self.connect(self.th2, QtCore.SIGNAL("finished()"), self.on_finished)
        self.connect(self.butNext, QtCore.SIGNAL('clicked()'), instance.next)
        self.connect(self.butPause, QtCore.SIGNAL('clicked()'), instance.pause)
        self.connect(self.butUnPause, QtCore.SIGNAL('clicked()'), instance.play)
        self.slider.sliderMoved.connect(self.handleSlider)
        self.dirname = None
        self.argv_play_count = 0
        if len(sys.argv) > 1:
            self.start()
    
    def reload_tracks(self):
        '''
        If playing - pause and load new tracks to list
        '''
        if instance.player.playing:
            instance.player.pause()
        instance.__init__()

    def start(self):  
        if len(sys.argv) > 1 and self.argv_play_count < 1:  # Play files from args 
            self.files = sys.argv[1:]
            self.reload_tracks()
            self.th2 = PlayThread(ex=instance, files=self.files)
            self.th2.start()
            self.th.start() 
            self.argv_play_count += 1 
        else:
            self.dirname = QtGui.QFileDialog.getExistingDirectory(self, 'Open file')  # Open file dialog

        if self.dirname:
            self.reload_tracks()
            self.th2 = PlayThread(ex=instance, files=fileGrabber.grabb_music_files_from_dir(self.dirname))
            self.th2.start()
            self.th.start()   

    def on_change(self, s, lst):
        self.labArt.setFixedHeight(300)
        self.labArt.setFixedWidth(300)
        database = DBConnect('GPlayer.db')
        try:
            data = database.get_image(unicode(s.encode('iso8859-1')))
            pm = QtGui.QPixmap()
            pm.loadFromData(QtCore.QByteArray(data))
            self.labArt.setPixmap(pm)
        except:
            self.labArt.setPixmap('logo.png')
        
        lst = [unicode(x.encode('iso8859-1')) for x in lst ]
        self.add_list(lst)  # add list to gui tracks table
        self.set_current(lst.index(instance.player.source.info.title or u'Unknown'))
        self.slider.setMaximum(instance.player.source.duration-1)
        self.slider.setValue(instance.player.time)
        #self.labArt.setPixmap(QtGui.QPixmap('logo.png'))

    def on_finished(self):
        pass

    def handleSlider(self, val):
        '''Seek if slider moved'''
        if val > 0:
            instance.player.seek(val)  
        else:
            instance.player.seek(val+1)      


app = QtGui.QApplication(sys.argv)
gui = Gui()    
gui.show()    
app.exec_()