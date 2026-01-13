from PySide6.QtCore import QRectF
from PySide6.QtGui import QPainter

from .baseobject import BaseObject
from .image import ImageObject
from .text import TextObject


class AnimationObject(BaseObject):
    TYPE = "Animation"

    OBJECT_TYPES = {
        "Image": ImageObject,
        "Text": TextObject,
    }

    ANIMATION_TYPES = {}

    def __init__(self, name="Animation1", parent=None):
        super().__init__(name=name, parent=parent)

        self.items = {}
        self.animations_dict = {}

    @classmethod
    def register_object_type(cls, obj_cls):
        cls.OBJECT_TYPES[obj_cls.TYPE] = obj_cls

    @classmethod
    def register_animation_type(cls, anim_cls):
        cls.ANIMATION_TYPES[anim_cls.TYPE] = anim_cls

    def boundingRect(self):
        return QRectF(0.0, 0.0, 0.0, 0.0)

    def paint(self, painter: QPainter, option, widget=None):
        return

    def _specific_to_dict(self):
        items_data = {}
        for uid, obj in self.items:
            items_data[str(uid)] = obj.to_dict()

        animations_data = {}
        for uid, anim_list in self.animations_dict:
            packed = []
            for anim in anim_list:
                packed.append(anim.to_dict())
            animations_data[str(uid)] = packed

        return {
            "items": items_data,
            "animations": animations_data,
        }

    def _specific_from_dict(self, data: dict):
        self.items = {}
        self.animations_dict = {}

        for uid, obj_data in data["items"].items():
            obj_cls = self.OBJECT_TYPES[obj_data["type"]]
            obj = obj_cls.create_obj(obj_data)
            self.items[uid] = obj

        for uid, anim_list in data["animations"].items():
            self.animations_dict[uid] = []
            for anim_data in anim_list:
                anim_cls = self.ANIMATION_TYPES[anim_data["type"]]
                anim = anim_cls.create_obj(anim_data)
                self.animations_dict[uid].append(anim)

