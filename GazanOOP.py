#!/usr/bin/python3
import pyglet
import time
import datetime
import sys, os
import datetime
import threading
import fileGrabber, PyQT
from db import DBConnect
from mutagen import File
from PIL import Image
from PySide2 import QtCore, QtGui, QtWidgets

class GazanPlayer():
    '''
    This is a player class. This class simply initializes player and
    creates methods for playing/pausing and for getting the next track
    '''

    def __init__(self):
        self.play_files = []  # List of track titles
        self.player = pyglet.media.Player()  # Initialize the player
        #self.player.eos_action = self.player.EOS_NEXT  # Not supported anymore
                
    def pause(self):  # Simple pause :-)
        self.player.pause()

    def play(self):  # Simple play :-)
        self.player.play()

    def next(self):  # Next :-)
        self.player.next_source()


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
            self.song.video_format = None # Workaround. Pyglet has segfaults when file is detected as audio
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
                gui.labTitle.setText(title)
                gui.labTitle.setToolTip(title)

                gui.labArtist.setText(author)
                gui.labArtist.setToolTip(author)

                gui.labAlbum.setText(album)
                gui.labAlbum.setToolTip(album)

                gui.labYear.setText(genre)
                gui.labYear.setToolTip(genre)

                # Display time
                gui.timer.display(datetime.datetime.fromtimestamp(self.instance.player.time).strftime('%M:%S')) 

                # Send signal every second   
                time.sleep(1)  
                a = self.instance.player.source.info.album
                self.signal_album.emit(a, self.instance.play_files)
            else:
                time.sleep(1)  # Sleep to avoid excessive CPU usage

    signal_album = QtCore.Signal(str, list)  # Define a new signal for PySide2

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
        self.butPlay.clicked.connect(self.start)
        self.th.signal_album.connect(self.on_change, QtCore.Qt.QueuedConnection)
        self.butNext.clicked.connect(instance.next)
        self.butPause.clicked.connect(instance.pause)
        self.butUnPause.clicked.connect(instance.play)
        self.slider.sliderMoved.connect(self.handleSlider)
        self.dirname = None
        self.argv_play_count = 0

        # Add a QTimer to process pyglet events
        self.qtimer = QtCore.QTimer()
        self.qtimer.timeout.connect(self.process_pyglet_events)
        self.qtimer.start(200)  # Process pyglet events every 200 ms

        if len(sys.argv) > 1:
            self.start()

    def process_pyglet_events(self):
        '''
        Process pyglet events periodically.
        Back in 2014,  `player.eos_action = player.EOS_NEXT` handled auto-advancing.
        However that is not supported anymore and EOS actions are implemented via events.
        https://pyglet.readthedocs.io/en/latest/programming_guide/media.html#ticking-the-clock
        '''
        pyglet.clock.tick()
        pyglet.app.platform_event_loop.step()

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
            self.dirname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open file')  # Open file dialog

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
            data = database.get_image(s)
            pm = QtGui.QPixmap()
            pm.loadFromData(data)
            self.labArt.setPixmap(pm)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.labArt.setPixmap(QtGui.QPixmap('logo.png'))
        
        self.add_list(lst)  # add list to gui tracks table
        self.set_current(lst.index(instance.player.source.info.title or u'Unknown'))
        self.slider.setMaximum(instance.player.source.duration-1)
        self.slider.setValue(instance.player.time)

    def on_finished(self):
        pass

    def handleSlider(self, val):
        '''Seek if slider moved'''
        if val > 0:
            instance.player.seek(val)  
        else:
            instance.player.seek(val+1)      


app = QtWidgets.QApplication(sys.argv)
gui = Gui()    
gui.show()    
app.exec_()
