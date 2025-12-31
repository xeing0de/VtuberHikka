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

    w = self.width()
    self.splitter.setSizes([int(w*0.55), int(w*0.45)])

    #panels
    self.left_panel = LeftPanel()
    self.right_panel = RightPanel()
    
    self.splitter.addWidget(self.left_panel)
    self.splitter.addWidget(self.right_panel)


  def on_button_click(self):
    self.label.setText("Кнопка нажата")


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())

