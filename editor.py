from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSplitter,
    QPushButton,
)
from PySide6.QtCore import Qt

from editorpanels import LeftPanelEditor
from editorpanels import CenterPanelEditor


class AnimationEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.obj = None

        main_layout = QVBoxLayout(self)

        editor_page = QWidget()
        editor_layout = QVBoxLayout(editor_page)

        self.splitter = QSplitter(Qt.Horizontal)
        editor_layout.addWidget(self.splitter)

        #panels
        self.left_panel = LeftPanelEditor()
        self.center_panel = CenterPanelEditor(scene=self.left_panel.scene)

        self.splitter.addWidget(self.left_panel)
        self.splitter.addWidget(self.center_panel)

        w = self.width()
        self.center_panel.setMinimumWidth(1)
        self.splitter.setSizes([int(w * 0.8), int(w * 0.2)])

        main_layout.addWidget(editor_page)

        #button
        self.btn_back = QPushButton("Back")
        main_layout.addWidget(self.btn_back)

    def set_animation(self, obj):
        self.obj = obj
        self.left_panel.set_animation(obj)
        self.center_panel.set_animation(obj)
