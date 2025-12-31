import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout
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

    label = QLabel("Hello world")
    label.setAlignment(Qt.AlignCenter)

    layout.addWidget(label)


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())

