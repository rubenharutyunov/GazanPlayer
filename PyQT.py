import sys
from PySide2 import QtCore, QtGui, QtWidgets

class PlayerGui(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PlayerGui, self).__init__(parent)

        self.lmain = QtWidgets.QGridLayout(self)
        self.layout = QtWidgets.QGridLayout()
        self.rlayout = QtWidgets.QHBoxLayout()
        self.table = QtWidgets.QTableView()
        self.installEventFilter(self)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setStyle(QtWidgets.QStyleFactory.create("windows"))
        self.slider.setStyleSheet(sliderCSS)
        self.slider.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.setGeometry(600, 300, 600, 500)
        self.setMinimumSize(400, 600)
        self.setWindowTitle("GazanPlayer v0.1")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))

        self.labArt = QtWidgets.QLabel("Album Art", self)
        self.labArt.setAlignment(QtCore.Qt.AlignHCenter)
        self.labArt.setPixmap(QtGui.QPixmap('logo.png'))
        self.labArt.setScaledContents(True)
        self.labArt.setStyleSheet('QLabel { border: 1px solid #cacaca; }')
        self.labTitle = QtWidgets.QLabel("Title", self)
        self.labArtist = QtWidgets.QLabel("Artist", self)
        self.labAlbum = QtWidgets.QLabel("Album", self)
        self.labYear = QtWidgets.QLabel("Year", self)

        self.timer = QtWidgets.QLCDNumber(self)
        self.timer.display("00:00")
        self.timer.setFixedHeight(50)
        self.timer.setFixedWidth(300)

        self.butPlay = QtWidgets.QPushButton("Play", self)
        self.butPause = QtWidgets.QPushButton("Pause", self)
        self.butUnPause = QtWidgets.QPushButton("Unpause", self)
        self.butExit = QtWidgets.QPushButton("Exit", self)
        self.butPrev = QtWidgets.QPushButton("< Prev", self)
        self.butNext = QtWidgets.QPushButton("Next >", self)

        horLine = QtWidgets.QFrame()
        horLine.setFrameStyle(QtWidgets.QFrame.HLine)
        horLine.setStyleSheet('QFrame {color: #a3a3a3}')

        labels = [self.labTitle, self.labArtist, self.labAlbum, self.labYear]
        self.layout.addItem(QtWidgets.QSpacerItem(0, 130), 2, 0, 2, 0)
        self.layout.addWidget(self.timer, 2, 0, 2, 0, QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.labArt, 0, 0, 1, 0, QtCore.Qt.AlignHCenter)
        for i in labels:
            i.setMaximumWidth(90)
            i.setStyleSheet('''QLabel { 
                                    border-style: solid;
                                    border-width: 1px;
                                    border-color: #cacaca;
                                    border-radius: 6px;
                                        }'''
                            )
            self.layout.addWidget(i, 1, labels.index(i), QtCore.Qt.AlignVCenter)

        self.lmain.setSpacing(10)
        self.layout.addWidget(self.butPrev, 4, 1)
        self.layout.addWidget(self.butNext, 4, 2)
        self.layout.addWidget(self.butPlay, 3, 0)
        self.layout.addWidget(self.butPause, 3, 1)
        self.layout.addWidget(self.butUnPause, 3, 2)
        self.layout.addWidget(self.butExit, 3, 3)
        self.rlayout.addWidget(self.table)

        self.lmain.addLayout(self.layout, 0, 0)
        self.lmain.addLayout(self.rlayout, 0, 1)
        self.lmain.addItem(QtWidgets.QSpacerItem(0, 20), 1, 0, 1, 0)
        self.lmain.addWidget(horLine, 2, 0, 2, 0)
        self.lmain.addItem(QtWidgets.QSpacerItem(0, 20), 3, 0, 3, 0)
        self.lmain.addWidget(self.slider, 4, 0, 4, 0)

        self.setLayout(self.lmain)

    def close(self):
        sys.exit()

    def add_list(self, lst):
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Tracks'])
        self.table.setModel(self.model)
        for i in lst:
            self.item = QtGui.QStandardItem(i)
            self.model.appendRow(self.item)
            self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def set_current(self, ind):
        self.index = self.model.index(ind, 0)
        self.table.setCurrentIndex(self.index)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.WindowActivate:
            self.setWindowOpacity(1)
        elif event.type() == QtCore.QEvent.WindowDeactivate:
            self.setWindowOpacity(0.8)

        return False

sliderCSS = '''QSlider::groove:horizontal {
border: 1px solid #bbb;
background: white;
height: 8px;
border-radius: 4px;
}

QSlider::sub-page:horizontal {
background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
    stop: 0 #fff, stop: 1 #999966);
background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
    stop: 0 #fff, stop: 1 #999966);
border: 1px solid #777;
height: 8px;
border-radius: 4px;
}

QSlider::add-page:horizontal {
background: #fff;
border: 1px solid #777;
height: 10px;
border-radius: 4px;
}

QSlider::handle:horizontal {
background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #eee, stop:1 #ccc);
border: 1px solid #777;
width: 13px;
margin-top: -2px;
margin-bottom: -2px;
border-radius: 5px;
}

QSlider::handle:horizontal:hover {
background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #fff, stop:1 #ddd);
border: 1px solid #444;
border-radius: 5px;
}

QSlider::sub-page:horizontal:disabled {
background: #bbb;
border-color: #999;
}

QSlider::add-page:horizontal:disabled {
background: #eee;
border-color: #999;
}

QSlider::handle:horizontal:disabled {
background: #eee;
border: 1px solid #aaa;
border-radius: 4px;
}'''
