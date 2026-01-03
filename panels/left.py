from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt

class LeftPanel(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)

    layout = QVBoxLayout(self)

    scene = QGraphicsScene(self)
    view = QGraphicsView(scene)

    pix = QPixmap("71.jpg")
    p = QPixmap("188.jpg").scaled(200,200)
    scene.addPixmap(pix)
    scene.addPixmap(p)

    view.setRenderHint(QPainter.Antialiasing)

    layout.addWidget(view)
