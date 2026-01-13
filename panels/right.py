from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
        QWidget, 
        QHBoxLayout, 
        QVBoxLayout, 
        QPushButton, 
        QLabel, 
        QSpinBox, 
        QFormLayout,
        QGroupBox,
        QListWidget,
        QListWidgetItem,
        )

from .properties import ImageProp

class RightPanel(QWidget):
    def __init__(self, project, scene = None, parent=None):
        super().__init__(parent)
        self.project = project
        self.scene = scene
        self.selected_object = None

        layout = QVBoxLayout(self)

        #buttons
        self.btn_load = QPushButton("Load Project")
        self.btn_save = QPushButton("Save Project")
        self.btn_limage = QPushButton("Load Image")
        self.btn_text = QPushButton("Add Text")
        self.btn_start = QPushButton("Start")

        #spinboxes
        self.sp_w = QSpinBox()
        self.sp_w.setRange(1, 20000)
        self.sp_w.setValue(800)

        self.sp_h = QSpinBox()
        self.sp_h.setRange(1, 20000)
        self.sp_h.setValue(500)

        #project
        gb_project = QGroupBox("Project")
        gb_project_layout = QVBoxLayout(gb_project)
        gb_project_layout.setContentsMargins(8, 10, 8, 8)
        gb_project_layout.setSpacing(6)

        project_row = QHBoxLayout()
        project_row.addWidget(self.btn_load)
        project_row.addWidget(self.btn_save)

        self.lbl_project_name = QLabel(f"Project name: {self.project.name}")

        gb_project_layout.addLayout(project_row)
        gb_project_layout.addWidget(self.lbl_project_name)

        #workspace
        gb_workspace = QGroupBox("Workspace")
        gb_workspace_layout = QVBoxLayout(gb_workspace)
        gb_workspace_layout.setContentsMargins(8, 10, 8, 8)
        gb_workspace_layout.setSpacing(6)
        
        workspace_row = QHBoxLayout()
        workspace_row.addWidget(QLabel("Width"))
        workspace_row.addWidget(self.sp_w)
        workspace_row.addWidget(QLabel("Height"))
        workspace_row.addWidget(self.sp_h)

        gb_workspace_layout.addLayout(workspace_row)

        #Layers
        gb_layers = QGroupBox("Layers")
        gb_layers_layout = QVBoxLayout(gb_layers)
        gb_layers_layout.setContentsMargins(8, 10, 8, 8)
        gb_layers_layout.setSpacing(6)

        self.layers_list = QListWidget()
        self.layers_list.setSelectionMode(QListWidget.SingleSelection)
        self.layers_list.itemSelectionChanged.connect(self._on_layer_selection_changed)
        gb_layers_layout.addWidget(self.layers_list)

        #toolbar
        gb_toolbar = QGroupBox("Toolbar")
        gb_toolbar_layout = QHBoxLayout(gb_toolbar)
        gb_toolbar_layout.setContentsMargins(8, 10, 8, 8)
        gb_toolbar_layout.setSpacing(6)

        gb_toolbar_layout.addWidget(self.btn_limage)
        gb_toolbar_layout.addWidget(self.btn_text)

        #object_properties
        gb_object = QGroupBox("Object")
        gb_object_layout = QVBoxLayout(gb_object)
        gb_object_layout.setContentsMargins(8, 10, 8, 8)
        gb_object_layout.setSpacing(6)
        
        self.obj_name = QLabel("Nothing Selected")
        gb_object_layout.addWidget(self.obj_name)
        self.prop = ImageProp(self.selected_object)
        gb_object_layout.addWidget(self.prop)

        #compose
        layout.addWidget(gb_project)
        layout.addWidget(gb_workspace)
        layout.addWidget(gb_toolbar)
        layout.addWidget(gb_layers)
        layout.addWidget(gb_object)

        layout.addStretch()

        layout.addWidget(self.btn_start)

    def set_selected_object(self, obj):
        self.selected_object = obj

        if obj is None:
            self.obj_name.setText("Nothing Selected")
        else:
            self.obj_name.setText(obj.type)

    def set_project(self, project):
        self.project = project
        self.lbl_project_name.setText(f"Project name: {self.project.name}")
        self.sp_w.setValue(self.project.output_width)
        self.sp_h.setValue(self.project.output_height)

    def refresh_layers(self):
        self.layers_list.blockSignals(True)
        self.layers_list.clear()

        items = self.project.items
        items.sort(key=lambda obj: obj._get_obj_z(), reverse=True)

        for obj in items:
            z = obj._get_obj_z()
            name = obj.name
            text = f"{z:g}. {name}"

            it = QListWidgetItem(text)
            it.setData(Qt.UserRole, obj)
            self.layers_list.addItem(it)

        if self.selected_object is not None:
            self._select_object_in_layers(self.selected_object)

        self.layers_list.blockSignals(False)

    def _select_object_in_layers(self, obj):
        for i in range(self.layers_list.count()):
            it = self.layers_list.item(i)
            if it.data(Qt.UserRole) is obj:
                self.layers_list.setCurrentRow(i)
                return

    def _on_layer_selection_changed(self):
        it = self.layers_list.currentItem()
        obj = it.data(Qt.UserRole) if it else None

        self.set_selected_object(obj)

        if obj is not None and self.scene is not None:
            self.scene.blockSignals(True)
            self.scene.clearSelection()
            obj.setSelected(True)
            self.scene.blockSignals(False)





