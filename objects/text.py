from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import (
    QPainter,
    QPen,
    QColor,
    QFont,
    QTextCharFormat,
    QTextCursor,
    QTextDocument,
    QPainterPath,
)
from PySide6.QtWidgets import QGraphicsItem

from .baseobject import BaseObject


class TextObject(BaseObject):
    TYPE = "Text"

    def __init__(
        self,
        text: str = "Text",
        name: str = "Text1",
        parent=None,
    ):
        super().__init__(name=name, parent=parent)

        self.text = text

        self.font_family = "Times New Roman"
        self.font_size = 14
        self.bold = False
        self.italic = False
        self.underline = False

        self.color = QColor(255, 255, 255, 255)

        self.outline_enabled = True
        self.outline_color = QColor(0, 0, 0, 255)
        self.outline_width = 2.0

        self._doc = QTextDocument()
        self._update_document()

    def _make_font(self):
        font = QFont(self.font_family, int(self.font_size))
        font.setBold(bool(self.bold))
        font.setItalic(bool(self.italic))
        font.setUnderline(bool(self.underline))
        return font

    def _apply_text_color(self):
        cursor = QTextCursor(self._doc)
        cursor.select(QTextCursor.Document)
        fmt = QTextCharFormat()
        fmt.setForeground(self.color)
        cursor.mergeCharFormat(fmt)

    def _update_document(self):
        self._doc.setDocumentMargin(0)
        self._doc.setDefaultFont(self._make_font())
        self._doc.setPlainText(self.text)

        self._doc.setTextWidth(-1)

        self._apply_text_color()

        self.prepareGeometryChange()
        self.update()

    def boundingRect(self) -> QRectF:
        size = self._doc.documentLayout().documentSize()
        return QRectF(0.0, 0.0, float(size.width()), float(size.height()))

    def paint(self, painter: QPainter, option, widget=None):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)

        font = self._make_font()
        painter.setFont(font)

        path = QPainterPath()

        block = self._doc.firstBlock()
        while block.isValid():
            layout = block.layout()
            line = layout.lineAt(0)

            x = line.position().x()
            y = line.position().y() + line.ascent()

            path.addText(x, y, font, block.text())

            block = block.next()

        if self.outline_enabled:
            pen = QPen(self.outline_color)
            pen.setWidthF(self.outline_width)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(path)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        painter.drawPath(path)

        painter.restore()

        if self.isSelected():
            self._paint_selection(painter)

    def _specific_to_dict(self):
        return {
            "text": self.text,
            "font_family": self.font_family,
            "font_size": float(self.font_size),
            "bold": bool(self.bold),
            "italic": bool(self.italic),
            "underline": bool(self.underline),
            "color": [
                self.color.red(),
                self.color.green(),
                self.color.blue(),
                self.color.alpha(),
            ],
            "outline_enabled": self.outline_enabled,
            "outline_width": float(self.outline_width),
            "outline_color": [
                self.outline_color.red(),
                self.outline_color.green(),
                self.outline_color.blue(),
                self.outline_color.alpha(),
            ],
        }

    def _specific_from_dict(self, data: dict):
        self.text = data.get("text", self.text)

        self.font_family = data.get("font_family", self.font_family)
        self.font_size = data.get("font_size", self.font_size)
        self.bold = data.get("bold", self.bold)
        self.italic = data.get("italic", self.italic)
        self.underline = data.get("underline", self.underline)

        col = data.get("color")
        if isinstance(col, (list, tuple)) and len(col) >= 3:
            self.color = QColor(
                int(col[0]),
                int(col[1]),
                int(col[2]),
                int(col[3]) if len(col) >= 4 else 255,
            )

        self.outline_enabled = data.get("outline_enabled", self.outline_enabled)
        self.outline_width = data.get("outline_width", self.outline_width)

        ocol = data.get("outline_color")
        if isinstance(ocol, (list, tuple)) and len(ocol) >= 3:
            self.outline_color = QColor(
                int(ocol[0]),
                int(ocol[1]),
                int(ocol[2]),
                int(ocol[3]) if len(ocol) >= 4 else 255,
            )

        self._update_document()

    def set_text(self, text: str):
        self.text = text
        self._update_document()

    def set_font(
        self,
        family: str = None,
        size: float = None,
        bold: bool = None,
        italic: bool = None,
        underline: bool = None,
    ):
        if family is not None:
            self.font_family = family
        if size is not None:
            self.font_size = size
        if bold is not None:
            self.bold = bold
        if italic is not None:
            self.italic = italic
        if underline is not None:
            self.underline = underline
        self._update_document()

    def set_color(self, color: QColor):
        self.color = color
        self._update_document()

