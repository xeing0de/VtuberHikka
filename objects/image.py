from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPainter, QPixmap, QPen, QColor
from PySide6.QtWidgets import QGraphicsItem

from .baseobject import BaseObject

class ImageObject(BaseObject):
    TYPE = "Image"

    def __init__(self, path: str = "", name: str = "Image1", parent=None):
        super().__init__(name=name, parent=parent)

        self.image_path = path
        self._pixmap = QPixmap(path)

    def boundingRect(self):
        return QRectF(self._pixmap.rect())

    def paint(self, painter: QPainter, option, widget=None):
        painter.drawPixmap(0, 0, self._pixmap)

        if self.isSelected():
            self._paint_selection(painter)

    def _specific_to_dict(self):
        return {
            "path": self.image_path,
        }

    def _specific_from_dict(self, data: dict):
        path = data["path"]
        self.image_path = path
        self._pixmap = QPixmap(path)

