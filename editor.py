from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt


class AnimationEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.obj = None

        layout = QVBoxLayout(self)

        self.title = QLabel("Animation editor")
        self.title.setAlignment(Qt.AlignCenter)

        self.btn_back = QPushButton("Back")

        layout.addWidget(self.title)
        layout.addWidget(self.btn_back)
        layout.addStretch(1)
