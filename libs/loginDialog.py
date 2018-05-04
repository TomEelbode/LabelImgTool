from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lib import newIcon
BB = QDialogButtonBox


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        layout = QVBoxLayout()

        self.explanation = QLabel("Who are you?")
        layout.addWidget(self.explanation)

        self.edit = QLineEdit()
        self.edit.setText(parent.username)

        layout.addWidget(self.edit)

        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon('done'))
        bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        self.setLayout(layout)

    def validate(self):
        if self.edit.text().strip():
            self.accept()

    def get_username(self):
        print self.edit.text()
        return self.edit.text().strip()
