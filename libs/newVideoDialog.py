from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt
from FrameGrabber import FrameGrabber
from lib import newIcon
BB = QDialogButtonBox


class NewVideoDialog(QDialog):
    """docstring for NewVideoDialog"""
    framestoskip = 0
    copyprevpred = False

    def __init__(self, parent=None, frameGrabber=None, config=None):
        super(NewVideoDialog, self).__init__(parent)
        if config is not None:
            self.__class__.framestoskip = config['framestoskip']
            self.__class__.copyprevpred = config['copyprevpred']

        self.frameGrabber = frameGrabber

        self.explanation = QLabel("Video loaded succesfully.")

        # Video filename
        self.filename = QLineEdit(frameGrabber.fp)
        self.filename.setReadOnly(True)

        # Video metadata
        self.framerate = QLineEdit(str(self.frameGrabber.get_fps()))
        self.framerate.setReadOnly(True)
        self.framerate.setAlignment(Qt.AlignRight)

        self.nb_frames = QLineEdit(str(self.frameGrabber.get_nframes()))
        self.nb_frames.setReadOnly(True)
        self.nb_frames.setAlignment(Qt.AlignRight)

        self.duration = QLineEdit(str(self.frameGrabber.get_duration()) + "s")
        self.duration.setReadOnly(True)
        self.duration.setAlignment(Qt.AlignRight)

        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)

        # Input how many frames to skip for annotation
        self.framestoskip = QLineEdit(parent=parent)
        self.framestoskip.setValidator(QIntValidator())
        self.framestoskip.setMaxLength(4)
        self.framestoskip.setAlignment(Qt.AlignRight)
        self.framestoskip.setText(str(self.__class__.framestoskip))

        # Decision buttons
        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon('done'))
        bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)

        # Check button indicating whether or not to copy previous prediction
        self.copyprevpred_cb = QtGui.QCheckBox("Copy last frame's prediction")
        self.copyprevpred_cb.setChecked(self.__class__.copyprevpred)
        self.copyprevpred_cb.stateChanged.connect(self.change_copyprevpred)

        # Add elements to layout
        formlayout = QFormLayout()
        formlayout.addRow(self.explanation)
        formlayout.addRow(hline)

        formlayout.addRow("Filename", self.filename)
        formlayout.addRow("FPS", self.framerate)
        formlayout.addRow("# frames", self.nb_frames)
        formlayout.addRow("Movie duration", self.duration)
        formlayout.addRow(hline)

        formlayout.addRow("Frames to skip", self.framestoskip)
        formlayout.addRow(self.copyprevpred_cb)

        layout = QVBoxLayout()
        layout.addLayout(formlayout, 1)
        layout.addWidget(bb)

        self.setLayout(layout)

        self.framestoskip.setFocus()
        self.show()

    def get_framesToSkip(self):
        return int(self.framestoskip.text().trimmed())

    def get_copyprevpred(self):
        return self.__class__.copyprevpred

    def validate(self):
        self.accept()

    def change_copyprevpred(self, state):
        if state == QtCore.Qt.Checked:
            self.__class__.copyprevpred = True
        else:
            self.__class__.copyprevpred = False
