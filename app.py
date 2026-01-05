import sys
from PySide6.QtWidgets import (
        QApplication,
        QMainWindow,
        QPushButton,
        QWidget,
        QVBoxLayout,
        QLabel,
        QSplitter,
        )
from PySide6.QtCore import Qt

from panels import LeftPanel, RightPanel
from buttons import UI
from objects import Project

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project = Project("empty")

        self.setWindowTitle("VTuberHikka")
        self.resize(600, 400)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        #splitter
        self.splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(self.splitter)

        #panels
        self.left_panel = LeftPanel(self.project)
        self.right_panel = RightPanel(self.project)

        self.splitter.addWidget(self.left_panel)
        self.splitter.addWidget(self.right_panel)

        w = self.width()
        self.splitter.setSizes([int(w*0.70), int(w*0.30)])

        #colors
        #self.left_panel.setStyleSheet("background-color: #2b2b2b;")
        #self.right_panel.setStyleSheet("background-color: #1e1e1e;")

        #buttons
        self.ui = UI(self)

        self.right_panel.btn_load.clicked.connect(self.ui.load_project)
        self.right_panel.btn_save.clicked.connect(self.ui.save_project)
        self.right_panel.btn_limage.clicked.connect(self.ui.load_image)

        self.right_panel.sp_w.valueChanged.connect(self.ui.work_space)
        self.right_panel.sp_h.valueChanged.connect(self.ui.work_space)

        #connections
        self.left_panel.on_object_selected = self.right_panel.set_selected_object

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.ui.work_space()
    sys.exit(app.exec())

