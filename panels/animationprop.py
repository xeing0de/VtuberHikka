from .baseprop import BaseProp
from PySide6.QtWidgets import QPushButton

class AnimationProp(BaseProp):
    def __init__(self, panel, obj=None, parent=None):
        super().__init__(panel=panel, obj=obj, parent=parent)

        self.btn_edit_animation = QPushButton("Edit animation")
        self.main_layout.addWidget(self.btn_edit_animation)
        self.main_layout.addStretch(1)

        self.set_object(obj)


