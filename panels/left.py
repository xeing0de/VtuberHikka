from PySide6.QtGui import QPixmap, QPainter, QPen, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene
from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtCore import Qt, QRectF, QPointF
from objects import ImageObject, Project


class GridScene(QGraphicsScene):
    def __init__(self, parent=None, grid_size=25):
        super().__init__(parent)
        self.grid_size = grid_size

    def drawBackground(self, painter: QPainter, rect: QRectF):
        super().drawBackground(painter, rect)

        pen = QPen(QColor(220, 220, 220))
        pen.setWidth(1)
        painter.setPen(pen)

        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)

        x = left
        while x < rect.right():
            painter.drawLine(x, rect.top(), x, rect.bottom())
            x += self.grid_size

        y = top
        while y < rect.bottom():
            painter.drawLine(rect.left(), y, rect.right(), y)
            y += self.grid_size


class LeftPanel(QWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.scene = GridScene(self, grid_size=25)
        self.view = QGraphicsView(self.scene)

        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)

        layout.addWidget(self.view)

        self.project = project 
        self._output_rect_item = None
        self._output_center = QPointF(184, 256)

    def set_project(self, project):
        self.project = project

        for item in list(self.scene.items()):
            if item is self._output_rect_item:
                continue
            self.scene.removeItem(item)

        for item in project.items:
            self.scene.addItem(item)

        self.update_output_rect(project.output_width, project.output_height)

    def update_output_rect(self, w, h):
        center = self._output_center

        rect = QRectF(center.x() - w / 2, center.y() - h / 2, w, h)

        if self._output_rect_item is None:
            self._output_rect_item = QGraphicsRectItem()
            pen = QPen(Qt.red)
            pen.setWidth(2)
            self._output_rect_item.setPen(pen)
            self._output_rect_item.setBrush(Qt.NoBrush)
            self._output_rect_item.setZValue(10**9)
            self.scene.addItem(self._output_rect_item)

            self._output_rect_item.setRect(rect)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.delete_selected_items()
        else:
            super().keyPressEvent(event)

    def delete_selected_items(self):
        selected_items = self.scene.selectedItems()

        for item in selected_items:
            self.scene.removeItem(item)
            self.project.items.remove(item)

