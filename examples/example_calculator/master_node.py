from qtpy.QtGui import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *

from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.utils import dumpException


class MasterGraphicsNode(QDMGraphicsNode):

    def initAssets(self):
        super().initAssets()
        pass


    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)
        self.icons = QImage("")
        painter.drawImage(QRectF(0, 0, 30, 30), self.icons)


    def UpdateIcon(self, icon: None):
        self.icons = QImage(icon)
        print(self.icons)


class MasterContent(QDMNodeContentWidget):
    def initUI(self):
        pass

class MasterNode(Node):
    icon = ""
    node_type = 0
    name = "Undefined"
    content_label = ""
    content_label_objname = "calc_node_bg"
    node_Value = None

    GraphicsNode_class = MasterGraphicsNode
    NodeContent_class = MasterContent

    def __init__(self, scene, inputs=[2,2], outputs=[1]):
        super().__init__(scene, self.__class__.name, inputs, outputs)
        self.NodeContent_class.initUI = self.initUI

    def initSettings(self):
        super().initSettings()
        pass

    def onInputChanged(self, socket=None):
        pass

    def serialize(self):
        res = super().serialize()
        res['node_type'] = self.__class__.node_type
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        # print("Deserialized Node '%s'" % self.__class__.__name__, "res:", res)
        return res