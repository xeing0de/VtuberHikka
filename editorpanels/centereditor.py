from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QGroupBox,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
)

from .imageprop import ImageProp
from .textprop import TextProp


class CenterPanelEditor(QWidget):
    def __init__(self, anim_obj=None, scene=None, parent=None):
        super().__init__(parent)

        self.anim_obj = None
        self.scene = scene

        self.selected_object = None
        self._uid_to_obj = {}

        self.on_add_image = None
        self.on_add_text = None

        layout = QVBoxLayout(self)

        # toolbar
        gb_toolbar = QGroupBox("Toolbar")
        gb_toolbar_layout = QHBoxLayout(gb_toolbar)
        gb_toolbar_layout.setContentsMargins(8, 10, 8, 8)
        gb_toolbar_layout.setSpacing(6)

        self.btn_add_image = QPushButton("Add Image")
        self.btn_add_text = QPushButton("Add Text")

        gb_toolbar_layout.addWidget(self.btn_add_image)
        gb_toolbar_layout.addWidget(self.btn_add_text)

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

        self.layers_list.setDragEnabled(True)
        self.layers_list.setAcceptDrops(True)
        self.layers_list.setDropIndicatorShown(True)
        self.layers_list.setDefaultDropAction(Qt.MoveAction)
        self.layers_list.setDragDropMode(QListWidget.InternalMove)

        gb_layers_layout.addWidget(self.layers_list)

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
        layout.addWidget(gb_toolbar)
        layout.addWidget(gb_layers)
        layout.addWidget(gb_object)

    def set_animation(self, anim_obj):
        self.anim_obj = anim_obj
        self.selected_object = None
        self._uid_to_obj = dict(self.anim_obj.items)
        self.refresh_layers()
        self.set_selected_object(None)

    def refresh_layers(self):
        self.layers_list.blockSignals(True)
        self.layers_list.clear()

        items = list(self.anim_obj.items.values())
        items.sort(key=lambda obj: obj._get_obj_z(), reverse=True)

        for obj in items:
            z = obj._get_obj_z()
            name = getattr(obj, "name", obj.type)
            text = f"{z:g}. {name}"

            it = QListWidgetItem(text)
            it.setData(Qt.UserRole, obj.uid)

            it.setFlags(it.flags() | Qt.ItemIsUserCheckable)
            it.setCheckState(Qt.Checked if obj.isVisible() else Qt.Unchecked)

            self.layers_list.addItem(it)

        self.layers_list.blockSignals(False)

        self._uid_to_obj = {o.uid: o for o in items}

        if self.selected_object is not None:
            self._select_object_in_layers(self.selected_object)

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

        self.refresh_layers()

class LayersList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.on_reorder = None

    def dropEvent(self, event):
        super().dropEvent(event)
        if self.on_reorder is not None:
            self.on_reorder()

