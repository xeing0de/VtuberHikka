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
from PySide6.QtGui import QPixmap

from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("VTuberHikka")
    self.resize(600, 400)
    
    central_widget = QWidget()
    self.setCentralWidget(central_widget)

    layout = QVBoxLayout()
    central_widget.setLayout(layout)

    #splitter
    self.splitter = QSplitter(Qt.Horizontal)
    layout.addWidget(self.splitter)
    
    #left panel
    self.left_panel = QWidget()
    left_layout = QVBoxLayout()
    self.left_panel.setLayout(left_layout)

    self.label = QLabel()
    pixmap = QPixmap("71.jpg")
    self.label.setPixmap(pixmap)

    left_layout.addWidget(self.label)

    #right panel
    self.right_panel = QWidget()
    right_layout = QVBoxLayout()
    self.right_panel.setLayout(right_layout)

    button = QPushButton("Load ")
    right_layout.addWidget(button)

    button.clicked.connect(self.on_button_click)

    w = self.width()
    self.splitter.setSizes([int(w*0.8), int(w*0.2)])
    
    self.splitter.addWidget(self.left_panel)
    self.splitter.addWidget(self.right_panel)


  def on_button_click(self):
    self.label.setText("Кнопка нажата")


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())

