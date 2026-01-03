from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPainter, QPixmap, QPen, QColor
from PySide6.QtWidgets import QGraphicsObject, QGraphicsItem

class ImageObject(QGraphicsObject):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.image_path = path
        self._pixmap = QPixmap(path) 

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
    
    def to_dict(self):
        pos = self.pos()
        return {
          "type": "image",
          "path": self.image_path,
          "x": float(pos.x()),
          "y": float(pos.y()),
          "scale": float(self.scale()),
          "rotation": float(self.rotation()),
          "z": float(self.zValue()),
          "opacity": float(self.opacity()),
          "visible": bool(self.isVisible()),
        }

    @staticmethod
    def from_dict(data):
        item = ImageObject(data["path"])
        item.setPos(data.get("x", 0.0), data.get("y", 0.0))
        item.setScale(data.get("scale", 1.0))
        item.setRotation(data.get("rotation", 0.0))
        item.setZValue(data.get("z", 0.0))
        item.setOpacity(data.get("opacity", 1.0))
        item.setVisible(data.get("visible", True))
        return item
