from abc import abstractmethod
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtWidgets import QGraphicsObject, QGraphicsItem


class BaseObject(QGraphicsObject):
    TYPE = "Base"
    def __init__(self, name: str = "Object", parent=None):
        super().__init__(parent)

        self.type = self.TYPE
        self.name = name

        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)

        self._selection_color = QColor(100, 100, 255)
        self._selection_width = 1.5

    @abstractmethod
    def boundingRect(self):
        pass

    @abstractmethod
    def paint(self, painter: QPainter, option, widget=None):
        pass

    @abstractmethod
    def _specific_to_dict(self):
        pass
    
    @abstractmethod
    def _specific_from_dict(self, data: dict):
        pass

    def _paint_selection(self, painter: QPainter):
        pen = QPen(self._selection_color)
        pen.setWidthF(self._selection_width)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(self.boundingRect())

    def to_dict(self):
        pos = self.pos()
        data = {
            "type": self.type,
            "name": self.name,

            "x": float(pos.x()),
            "y": float(pos.y()),
            "scale": float(self.scale()),
            "rotation": float(self.rotation()),
            "z": float(self.zValue()),
            "opacity": float(self.opacity()),
            "visible": bool(self.isVisible()),
        }
        data.update(self._specific_to_dict())
        return data

    def from_dict(self, data: dict):
        self.name = data.get("name", self.name)
        self.type = data.get("type", self.type)

        self.setPos(data.get("x", 0.0), data.get("y", 0.0))
        self.setScale(data.get("scale", 1.0))
        self.setRotation(data.get("rotation", 0.0))
        self.setZValue(data.get("z", 0.0))
        self.setOpacity(data.get("opacity", 1.0))
        self.setVisible(data.get("visible", True))
        self._specific_from_dict(data)

    @classmethod
    def create_obj(cls, data: dict):
        item = cls()
        item.from_dict(data)
        return item

