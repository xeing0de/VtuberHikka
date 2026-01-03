from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPainter, QPixmap, QPen, QColor
from PySide6.QtWidgets import QGraphicsObject, QGraphicsItem

class ImageObject(QGraphicsObject):
  def __init__(self, pixmap, parent=None):
    super().__init__(parent)
    self._pixmap = QPixmap(pixmap) 

    self.setFlag(QGraphicsItem.ItemIsSelectable, True)
    self.setFlag(QGraphicsItem.ItemIsMovable, True)

  def boundingRect(self):
    return QRectF(self._pixmap.rect())

  def paint(self, painter: QPainter, option, widget=None):
    painter.drawPixmap(0, 0, self._pixmap)

    if self.isSelected():
        pen = QPen(QColor(100, 100, 255))
        pen.setWidthF(1.5)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        painter.drawRect(self._pixmap.rect())
