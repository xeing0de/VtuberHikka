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

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("VTuberHikka")
    self.resize(600, 400)
    
    central = QWidget()
    self.setCentralWidget(central)
    layout = QVBoxLayout(central)

    #splitter
    self.splitter = QSplitter(Qt.Horizontal)
    layout.addWidget(self.splitter)

    #panels
    self.left_panel = LeftPanel()
    self.right_panel = RightPanel()
    
    self.splitter.addWidget(self.left_panel)
    self.splitter.addWidget(self.right_panel)

    w = self.width()
    self.splitter.setSizes([int(w*0.55), int(w*0.45)])

    #colors
    #self.left_panel.setStyleSheet("background-color: #2b2b2b;")
    #self.right_panel.setStyleSheet("background-color: #1e1e1e;")

    #buttons
    self.ui = UI(self)
    self.right_panel.btn_load.clicked.connect(self.ui.load_project)

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())

