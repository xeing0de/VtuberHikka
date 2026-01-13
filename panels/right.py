from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QSpinBox,
    QGroupBox,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
)

from .imageprop import ImageProp
from .textprop import TextProp


class RightPanel(QWidget):
    def __init__(self, project, scene=None, parent=None):
        super().__init__(parent)
        self.project = project
        self.scene = scene
        self.selected_object = None
        self._uid_to_obj = {o.uid: o for o in self.project.items}

        layout = QVBoxLayout(self)

        # buttons
        self.btn_load = QPushButton("Load Project")
        self.btn_save = QPushButton("Save Project")
        self.btn_limage = QPushButton("Load Image")
        self.btn_text = QPushButton("Add Text")
        self.btn_start = QPushButton("Start")
        self.btn_animation = QPushButton("Create Animation")

        # spinboxes
        self.sp_w = QSpinBox()
        self.sp_w.setRange(1, 20000)
        self.sp_w.setValue(800)

        self.sp_h = QSpinBox()
        self.sp_h.setRange(1, 20000)
        self.sp_h.setValue(500)

        # project
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

        # workspace
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

        # layers
        gb_layers = QGroupBox("Layers")
        gb_layers_layout = QVBoxLayout(gb_layers)
        gb_layers_layout.setContentsMargins(8, 10, 8, 8)
        gb_layers_layout.setSpacing(6)

        self.layers_list = LayersList()
        self.layers_list.on_reorder = self._on_layers_reordered
        self.layers_list.setSelectionMode(QListWidget.SingleSelection)
        self.layers_list.itemSelectionChanged.connect(self._on_layer_selection_changed)
        self.layers_list.itemChanged.connect(self._on_layer_item_changed)
        gb_layers_layout.addWidget(self.layers_list)

        self.layers_list.setDragEnabled(True)
        self.layers_list.setAcceptDrops(True)
        self.layers_list.setDropIndicatorShown(True)
        self.layers_list.setDefaultDropAction(Qt.MoveAction)
        self.layers_list.setDragDropMode(QListWidget.InternalMove)

        # toolbar
        gb_toolbar = QGroupBox("Toolbar")
        gb_toolbar_layout = QHBoxLayout(gb_toolbar)
        gb_toolbar_layout.setContentsMargins(8, 10, 8, 8)
        gb_toolbar_layout.setSpacing(6)

        gb_toolbar_layout.addWidget(self.btn_limage)
        gb_toolbar_layout.addWidget(self.btn_text)
        gb_toolbar_layout.addWidget(self.btn_animation)

        # object properties
        gb_object = QGroupBox("Object")
        gb_object_layout = QVBoxLayout(gb_object)
        gb_object_layout.setContentsMargins(8, 10, 8, 8)
        gb_object_layout.setSpacing(6)

        self.obj_name = QLabel("Nothing Selected")
        gb_object_layout.addWidget(self.obj_name)

        self.props_stack = QStackedWidget()
        gb_object_layout.addWidget(self.props_stack)

        self.empty_prop = QLabel("No properties")
        self.empty_prop.setAlignment(Qt.AlignCenter)
        self.props_stack.addWidget(self.empty_prop)

        self.prop_dict = {
            "Image": ImageProp(self, None),
            "Text": TextProp(self, None),
        }

        for w in self.prop_dict.values():
            self.props_stack.addWidget(w)

        self.props_stack.setCurrentWidget(self.empty_prop)

        # compose
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
            self.props_stack.setCurrentWidget(self.empty_prop)
            return

        self.obj_name.setText(obj.type)

        prop = self.prop_dict.get(obj.type)
        if prop is None:
            self.props_stack.setCurrentWidget(self.empty_prop)
            return

        self.props_stack.setCurrentWidget(prop)
        prop.set_object(obj)

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
            it.setData(Qt.UserRole, obj.uid)

            it.setFlags(it.flags() | Qt.ItemIsUserCheckable)
            it.setCheckState(Qt.Checked if obj.isVisible() else Qt.Unchecked)

            self.layers_list.addItem(it)

        if self.selected_object is not None:
            self._select_object_in_layers(self.selected_object)

        self.layers_list.blockSignals(False)
        self._uid_to_obj = {o.uid: o for o in self.project.items}

    def _select_object_in_layers(self, obj):
        for i in range(self.layers_list.count()):
            it = self.layers_list.item(i)
            if it.data(Qt.UserRole) == obj.uid:
                self.layers_list.setCurrentRow(i)
                return

    def _on_layer_item_changed(self, item):
        uid = item.data(Qt.UserRole)
        obj = self._uid_to_obj.get(uid) if uid else None
        if obj is None:
            return

        visible = item.checkState() == Qt.Checked
        obj.setVisible(visible)

        if obj is self.selected_object:
            w = self.props_stack.currentWidget()
            if hasattr(w, "pull_from_object"):
                w.pull_from_object()


    def _on_layer_selection_changed(self):
        it = self.layers_list.currentItem()
        uid = it.data(Qt.UserRole) if it else None
        obj = self._uid_to_obj.get(uid) if uid else None

        self.set_selected_object(obj)

        if obj is not None and self.scene is not None:
            self.scene.blockSignals(True)
            self.scene.clearSelection()
            obj.setSelected(True)
            self.scene.blockSignals(False)

    def _on_layers_reordered(self):
        count = self.layers_list.count()

        for i in range(count):
            item = self.layers_list.item(i)
            uid = item.data(Qt.UserRole)
            obj = self._uid_to_obj.get(uid)

            new_z = count - 1 - i
            obj.setZValue(new_z)

        self.project.items.sort(key=lambda o: o.zValue())
        self.refresh_layers()


class LayersList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.on_reorder = None

    def dropEvent(self, event):
        super().dropEvent(event)
        if self.on_reorder is not None:
            self.on_reorder()

