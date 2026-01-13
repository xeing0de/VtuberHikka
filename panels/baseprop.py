from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QDoubleSpinBox,
    QCheckBox,
    QFormLayout,
    QLineEdit,
)

class BaseProp(QWidget):
    def __init__(self, panel, obj=None, parent=None):
        super().__init__(parent)
        self.obj = None
        self._updating = False
        self.panel = panel

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(6)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignLeft)
        form.setHorizontalSpacing(8)
        form.setVerticalSpacing(6)

        self.ed_name = QLineEdit()
        form.addRow("Name", self.ed_name)

        self.sp_x = QDoubleSpinBox()
        self.sp_x.setRange(-100000, 100000)
        self.sp_x.setDecimals(2)

        self.sp_y = QDoubleSpinBox()
        self.sp_y.setRange(-100000, 100000)
        self.sp_y.setDecimals(2)

        pos_row = QHBoxLayout()
        pos_row.addWidget(QLabel("X"))
        pos_row.addWidget(self.sp_x)
        pos_row.addWidget(QLabel("Y"))
        pos_row.addWidget(self.sp_y)
        form.addRow("Position", pos_row)

        self.sp_scale = QDoubleSpinBox()
        self.sp_scale.setRange(0.01, 1000.0)
        self.sp_scale.setDecimals(3)
        form.addRow("Scale", self.sp_scale)

        self.sp_rotation = QDoubleSpinBox()
        self.sp_rotation.setRange(-360.0, 360.0)
        self.sp_rotation.setDecimals(2)
        form.addRow("Rotation", self.sp_rotation)

        self.sp_opacity = QDoubleSpinBox()
        self.sp_opacity.setRange(0.0, 1.0)
        self.sp_opacity.setSingleStep(0.05)
        self.sp_opacity.setDecimals(2)
        form.addRow("Opacity", self.sp_opacity)

        main_layout.addLayout(form)

        self._connect_signals()
        self.set_object(obj)

    def _connect_signals(self):
        self.ed_name.editingFinished.connect(self._on_name_changed)
        self.sp_x.valueChanged.connect(self._on_pos_changed)
        self.sp_y.valueChanged.connect(self._on_pos_changed)
        self.sp_scale.valueChanged.connect(self._on_scale_changed)
        self.sp_rotation.valueChanged.connect(self._on_rotation_changed)
        self.sp_opacity.valueChanged.connect(self._on_opacity_changed)

    def set_object(self, obj):
        self.obj = obj
        self.setEnabled(obj is not None)
        self.pull_from_object()

    def pull_from_object(self):
        self._updating = True
        try:
            if self.obj is None:
                self.ed_name.setText("")
                self.sp_x.setValue(0.0)
                self.sp_y.setValue(0.0)
                self.sp_scale.setValue(1.0)
                self.sp_rotation.setValue(0.0)
                self.sp_opacity.setValue(1.0)
                return

            self.ed_name.setText(getattr(self.obj, "name", ""))

            p = self.obj.pos()
            self.sp_x.setValue(float(p.x()))
            self.sp_y.setValue(float(p.y()))
            self.sp_scale.setValue(float(self.obj.scale()))
            self.sp_rotation.setValue(float(self.obj.rotation()))
            self.sp_opacity.setValue(float(self.obj.opacity()))
        finally:
            self._updating = False

    def _on_name_changed(self):
        if self._updating or self.obj is None:
            return

        name = self.ed_name.text().strip()
        if not name:
            return

        self.obj.name = name
        self.panel.refresh_layers()

    def _on_pos_changed(self):
        if self._updating or self.obj is None:
            return
        self.obj.setPos(self.sp_x.value(), self.sp_y.value())

    def _on_scale_changed(self, v):
        if self._updating or self.obj is None:
            return
        self.obj.setScale(v)

    def _on_rotation_changed(self, v):
        if self._updating or self.obj is None:
            return
        self.obj.setRotation(v)

    def _on_opacity_changed(self, v):
        if self._updating or self.obj is None:
            return
        self.obj.setOpacity(v)

