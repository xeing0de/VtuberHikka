from PySide6.QtGui import QPixmap, QPainter, QPen, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene
from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtCore import Qt, QRectF, QPointF
from objects import ImageObject, Project


class GridScene(QGraphicsScene):
    def __init__(self, parent=None, grid_size=25):
        super().__init__(parent)
        self.grid_size = grid_size
        self.grid_center = QPointF(184, 256)

    def drawBackground(self, painter: QPainter, rect: QRectF):
        super().drawBackground(painter, rect)
        
        pen = QPen(QColor(220, 220, 220))
        pen.setWidth(1)
        painter.setPen(pen)

        gs = self.grid_size
        cx = self.grid_center.x()
        cy = self.grid_center.y()

        left = rect.left() - ((rect.left() - cx) % gs)
        right = rect.right()
        top = rect.top() - ((rect.top() - cy) % gs)
        bottom = rect.bottom()

        x = left
        while x <= right:
            painter.drawLine(x, top, x, bottom)
            x += gs

        y = top
        while y <= bottom:
            painter.drawLine(left, y, right, y)
            y += gs

        pen = QPen(QColor(255, 0, 0))
        pen.setWidth(2)
        painter.setPen(pen)

        cross = 20
        painter.drawLine(cx - cross, cy, cx + cross, cy)
        painter.drawLine(cx, cy - cross, cx, cy + cross)

class LeftPanel(QWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.scene = GridScene(self, grid_size=25)
        self.scene.selectionChanged.connect(self._selection_changed)

        self.view = QGraphicsView(self.scene)

        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)

        layout.addWidget(self.view)

        self.project = project 
        self._output_rect_item = None
        self._output_center = QPointF(184, 256)
        self.on_object_selected = None
        self.on_set_project = None
        self.on_items_changed = None

    def set_project(self, project):
        self.project = project

        for item in list(self.scene.items()):
            if item is self._output_rect_item:
                continue
            self.scene.removeItem(item)

        for item in project.items:
            self.scene.addItem(item)

        self.update_output_rect(project.output_width, project.output_height)
        self.on_set_project(self.project)
        self.on_items_changed()

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
            self.project.delete_item(item)

        self.on_items_changed()

    def _selection_changed(self):
        items = self.scene.selectedItems()
        selected = items[0] if items else None

        if self.on_object_selected is not None:
            self.on_object_selected(selected)
        
        self.on_items_changed()
