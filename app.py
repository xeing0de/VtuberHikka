import sys
from PySide6.QtWidgets import (
        QApplication,
        QMainWindow,
        QPushButton,
        QWidget,
        QVBoxLayout,
        QLabel,
        QSplitter,
        QStackedWidget,
        )
from PySide6.QtCore import Qt

from panels import LeftPanel, RightPanel
from buttons import UI
from objects import Project
from editor import AnimationEditor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project = Project("empty")

        self.setWindowTitle("VTuberHikka")
        self.resize(600, 400)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        #stack
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        ##main_window
        editor_page = QWidget()
        editor_layout = QVBoxLayout(editor_page)

        #splitter
        self.splitter = QSplitter(Qt.Horizontal)
        editor_layout.addWidget(self.splitter)

        #panels
        self.left_panel = LeftPanel(self.project)
        self.right_panel = RightPanel(self.project, scene=self.left_panel.scene)

        self.splitter.addWidget(self.left_panel)
        self.splitter.addWidget(self.right_panel)

        w = self.width()
        self.right_panel.setMinimumWidth(1)
        self.splitter.setSizes([int(w * 0.8), int(w * 0.2)])

        self.stack.addWidget(editor_page)

        ##editor
        self.anim_editor = AnimationEditor()
        self.stack.addWidget(self.anim_editor)

        #buttons
        self.ui = UI(self)

        self.right_panel.btn_load.clicked.connect(self.ui.load_project)
        self.right_panel.btn_save.clicked.connect(self.ui.save_project)
        self.right_panel.btn_limage.clicked.connect(self.ui.load_image)
        self.right_panel.btn_text.clicked.connect(self.ui.create_text)
        self.right_panel.btn_animation.clicked.connect(self.ui.create_animation)
        self.anim_editor.btn_back.clicked.connect(self._exit_animation_editor)
        self.anim_editor.center_panel.btn_add_text.clicked.connect(self.ui.create_text_anim)

        self.right_panel.sp_w.valueChanged.connect(self.ui.work_space)
        self.right_panel.sp_h.valueChanged.connect(self.ui.work_space)

        #connections
        self.left_panel.on_object_selected = self.right_panel.set_selected_object
        self.left_panel.on_set_project = self.right_panel.set_project
        self.left_panel.on_items_changed = self.right_panel.refresh_layers
        self.anim_editor.left_panel.on_items_changed = self.anim_editor.center_panel.refresh_layers
        self.right_panel.edit_animation = self._enter_editor

    def _enter_editor(self, anim_obj):
        self.anim_editor.set_animation(anim_obj)
        self.stack.setCurrentIndex(1)

    def _exit_animation_editor(self):
        self.stack.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.ui.work_space()
    sys.exit(app.exec())

