import uuid

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
        self.z = 0

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
        for uid, obj in self.items.items():
            items_data[str(uid)] = obj.to_dict()

        animations_data = {}
        for uid, anim_list in self.animations_dict.items():
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
    
    def add_item(self, item):
        item_uid = uuid.uuid4().hex
        item.setZValue(self.z)
        self.items[item_uid] = item
        self.z += 1

    def delete_item(self, item):
        uid_to_delete = None
        for uid, obj in self.items.items():
            if obj is item:
                uid_to_delete = uid
                break

        del self.items[uid_to_delete]
        self._normalize_z()

    def _normalize_z(self):
        ordered = sorted(self.items.values(), key=lambda it: it.zValue())
        for i, obj in enumerate(ordered):
            obj.setZValue(i)
        self.z = len(ordered)

