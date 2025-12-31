import sys
from PySide6.QtWidgets import (
  QApplication,
  QMainWindow,
  QPushButton,
  QWidget,
  QVBoxLayout,
  QLabel,
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

    self.label = QLabel("Hello world")
    self.label.setAlignment(Qt.AlignCenter)

    button = QPushButton("Load ")
    layout.addWidget(button)

    pixmap = QPixmap("71.jpg")
    self.label.setPixmap(pixmap)

    layout.addWidget(self.label)

    button.clicked.connect(self.on_button_click)

  def on_button_click(self):
    self.label.setText("Кнопка нажата")


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())

