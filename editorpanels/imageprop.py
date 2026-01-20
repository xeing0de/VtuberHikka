from .baseprop import BaseProp


class ImageProp(BaseProp):
    def __init__(self, panel, obj=None, parent=None):
        super().__init__(panel=panel, obj=obj, parent=parent)
        self.set_object(obj)

