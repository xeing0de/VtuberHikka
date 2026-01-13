from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QWidget,
    QColorDialog,
)

from .baseprop import BaseProp


class TextProp(BaseProp):
    def __init__(self, panel, obj=None, parent=None):
        super().__init__(panel=panel, obj=None, parent=parent)

        self._extra_form = QFormLayout()
        self._extra_form.setLabelAlignment(Qt.AlignLeft)
        self._extra_form.setHorizontalSpacing(8)
        self._extra_form.setVerticalSpacing(6)
        self.main_layout.addLayout(self._extra_form)

        self.ed_text = QTextEdit()
        self.ed_text.setAcceptRichText(False)
        self.ed_text.setMinimumHeight(80)
        self._extra_form.addRow("Text", self.ed_text)

        self.cb_family = QComboBox()
        self.cb_family.setEditable(True)
        self.cb_family.addItems(
            [
                "Times New Roman",
                "Arial",
                "Verdana",
                "Tahoma",
                "Courier New",
            ]
        )
        self._extra_form.addRow("Font", self.cb_family)

        self.sp_size = QDoubleSpinBox()
        self.sp_size.setRange(1.0, 512.0)
        self.sp_size.setDecimals(1)
        self.sp_size.setSingleStep(1.0)
        self._extra_form.addRow("Size", self.sp_size)

        flags_row = QHBoxLayout()
        flags_row.setContentsMargins(0, 0, 0, 0)
        self.ch_bold = QCheckBox("Bold")
        self.ch_italic = QCheckBox("Italic")
        self.ch_underline = QCheckBox("Underline")
        flags_row.addWidget(self.ch_bold)
        flags_row.addWidget(self.ch_italic)
        flags_row.addWidget(self.ch_underline)

        flags_holder = QWidget()
        flags_holder.setLayout(flags_row)
        self._extra_form.addRow("Style", flags_holder)

        self.lbl_color = QLabel()
        self.lbl_color.setFixedWidth(42)
        self.lbl_color.setFixedHeight(18)
        self.btn_color = QPushButton("Pick")

        color_row = QHBoxLayout()
        color_row.setContentsMargins(0, 0, 0, 0)
        color_row.addWidget(self.lbl_color)
        color_row.addWidget(self.btn_color)

        color_holder = QWidget()
        color_holder.setLayout(color_row)
        self._extra_form.addRow("Color", color_holder)

        self.ch_outline = QCheckBox("Enabled")
        self._extra_form.addRow("Outline", self.ch_outline)

        self.sp_outline_w = QDoubleSpinBox()
        self.sp_outline_w.setRange(0.0, 100.0)
        self.sp_outline_w.setDecimals(2)
        self.sp_outline_w.setSingleStep(0.5)
        self._extra_form.addRow("Outline width", self.sp_outline_w)

        self.lbl_outline_color = QLabel()
        self.lbl_outline_color.setFixedWidth(42)
        self.lbl_outline_color.setFixedHeight(18)
        self.btn_outline_color = QPushButton("Pick")

        ocol_row = QHBoxLayout()
        ocol_row.setContentsMargins(0, 0, 0, 0)
        ocol_row.addWidget(self.lbl_outline_color)
        ocol_row.addWidget(self.btn_outline_color)

        ocol_holder = QWidget()
        ocol_holder.setLayout(ocol_row)
        self._extra_form.addRow("Outline color", ocol_holder)

        self.ed_text.textChanged.connect(self._on_text_changed)
        self.cb_family.currentTextChanged.connect(self._on_font_changed)
        self.sp_size.valueChanged.connect(self._on_font_changed)
        self.ch_bold.toggled.connect(self._on_font_changed)
        self.ch_italic.toggled.connect(self._on_font_changed)
        self.ch_underline.toggled.connect(self._on_font_changed)
        self.btn_color.clicked.connect(self._on_pick_color)

        self.ch_outline.toggled.connect(self._on_outline_changed)
        self.sp_outline_w.valueChanged.connect(self._on_outline_changed)
        self.btn_outline_color.clicked.connect(self._on_pick_outline_color)

        self.set_object(obj)

    def pull_from_object(self):
        super().pull_from_object()

        self._updating = True
        try:
            if self.obj is None:
                self.ed_text.setPlainText("")
                self.cb_family.setCurrentText("Times New Roman")
                self.sp_size.setValue(14.0)
                self.ch_bold.setChecked(False)
                self.ch_italic.setChecked(False)
                self.ch_underline.setChecked(False)
                self._set_color_preview(self.lbl_color, QColor(255, 255, 255, 255))
                self.ch_outline.setChecked(False)
                self.sp_outline_w.setValue(2.0)
                self._set_color_preview(self.lbl_outline_color, QColor(0, 0, 0, 255))
                return

            self.ed_text.setPlainText(getattr(self.obj, "text", ""))
            self.cb_family.setCurrentText(getattr(self.obj, "font_family", "Times New Roman"))
            self.sp_size.setValue(float(getattr(self.obj, "font_size", 14.0)))
            self.ch_bold.setChecked(bool(getattr(self.obj, "bold", False)))
            self.ch_italic.setChecked(bool(getattr(self.obj, "italic", False)))
            self.ch_underline.setChecked(bool(getattr(self.obj, "underline", False)))

            self._set_color_preview(
                self.lbl_color,
                getattr(self.obj, "color", QColor(255, 255, 255, 255)),
            )

            self.ch_outline.setChecked(bool(getattr(self.obj, "outline_enabled", False)))
            self.sp_outline_w.setValue(float(getattr(self.obj, "outline_width", 2.0)))
            self._set_color_preview(
                self.lbl_outline_color,
                getattr(self.obj, "outline_color", QColor(0, 0, 0, 255)),
            )
        finally:
            self._updating = False

    def _set_color_preview(self, label: QLabel, color: QColor):
        label.setStyleSheet(
            "QLabel {"
            "border: 1px solid rgba(0,0,0,120);"
            f"background: rgba({color.red()},{color.green()},{color.blue()},{color.alpha()});"
            "}"
        )

    def _on_text_changed(self):
        if self._updating or self.obj is None:
            return
        self.obj.set_text(self.ed_text.toPlainText())

    def _on_font_changed(self, *_):
        if self._updating or self.obj is None:
            return
        self.obj.set_font(
            family=self.cb_family.currentText(),
            size=float(self.sp_size.value()),
            bold=bool(self.ch_bold.isChecked()),
            italic=bool(self.ch_italic.isChecked()),
            underline=bool(self.ch_underline.isChecked()),
        )

    def _on_pick_color(self):
        if self.obj is None:
            return
        current = getattr(self.obj, "color", QColor(255, 255, 255, 255))
        col = QColorDialog.getColor(current, self, "Select color")
        if not col.isValid():
            return
        self.obj.set_color(col)
        self._set_color_preview(self.lbl_color, col)

    def _on_outline_changed(self, *_):
        if self._updating or self.obj is None:
            return

        self.obj.outline_enabled = bool(self.ch_outline.isChecked())
        self.obj.outline_width = float(self.sp_outline_w.value())
        self.obj._update_document()

    def _on_pick_outline_color(self):
        if self.obj is None:
            return
        current = getattr(self.obj, "outline_color", QColor(0, 0, 0, 255))
        col = QColorDialog.getColor(current, self, "Select outline color")
        if not col.isValid():
            return
        self.obj.outline_color = col
        self.obj._update_document()
        self._set_color_preview(self.lbl_outline_color, col)

