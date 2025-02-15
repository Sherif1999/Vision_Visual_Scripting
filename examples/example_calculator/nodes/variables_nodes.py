from PyQt5.QtGui import QBrush, QColor

from examples.example_calculator.nodes.default_functions import FontSize, FontFamily
from examples.example_calculator.nodes.nodes_configuration import *
from examples.example_calculator.master_node import MasterNode

FloatColor = "#7000FF10"
IntegerColor = "#aa0070FF"
BooleanColor = "#aaFF1010"
StringColor = "#70FF10FF"

@set_var_ID(VAR_FLOAT)
class FloatVar(MasterNode):
    icon = ""
    node_type = VAR_FLOAT
    name = "float"
    content_label_objname = "var_node_float"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[1])
        self.isVar = True
        self.grNode._brush_title = QBrush(QColor(FloatColor))

    def toGetter(self):
        self.isSetter = False
        self.initSockets(inputs=[], outputs=[1])
        self.getNodeCode = self.getterCode

    def toSetter(self):
        self.isSetter = True
        self.initSockets(inputs=[0, 1], outputs=[0])
        self.getNodeCode = self.setterCode

    def getterCode(self):
        self.showCode = False
        getCode = self.name
        return getCode

    def setterCode(self):
        self.showCode = not self.isInputConnected(0)
        brotherCode = self.NodeCodeAtOutput(0)
        setInput = self.NodeCodeAtInput(1)

        setCode = f"""
{self.name}={setInput}
{brotherCode}"""

        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{FloatColor};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{setCode}</span></p></pre> """

        return code


@set_var_ID(VAR_INTEGER)
class IntegerVar(MasterNode):
    icon = ""
    node_type = VAR_INTEGER
    name = "integer"
    content_label_objname = "var_node_integer"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[2])
        self.isVar = True
        self.grNode._brush_title = QBrush(QColor(IntegerColor))

    def toGetter(self):
        self.isSetter = False
        self.initSockets(inputs=[], outputs=[2])
        self.getNodeCode = self.getterCode

    def toSetter(self):
        self.isSetter = True
        self.initSockets(inputs=[0, 2], outputs=[0])
        self.getNodeCode = self.setterCode

    def getterCode(self):
        self.showCode = False
        getCode = self.name
        return getCode

    def setterCode(self):
        self.showCode = not self.isInputConnected(0)
        brotherCode = self.NodeCodeAtOutput(0)
        setInput = self.NodeCodeAtInput(1)

        setCode = f"""
{self.name}={setInput}
{brotherCode}"""

        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{IntegerColor};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{setCode}</span></p></pre> """

        return code


@set_var_ID(VAR_BOOLEAN)
class BooleanVar(MasterNode):
    icon = ""
    node_type = VAR_BOOLEAN
    name = "boolean"
    content_label_objname = "var_node_boolean"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])
        self.isVar = True
        self.grNode._brush_title = QBrush(QColor(BooleanColor))

    def toGetter(self):
        self.isSetter = False
        self.initSockets(inputs=[], outputs=[3])
        self.getNodeCode = self.getterCode

    def toSetter(self):
        self.isSetter = True
        self.initSockets(inputs=[0, 3], outputs=[0])
        self.getNodeCode = self.setterCode

    def getterCode(self):
        self.showCode = False
        getCode = self.name
        return getCode

    def setterCode(self):
        self.showCode = not self.isInputConnected(0)
        brotherCode = self.NodeCodeAtOutput(0)
        setInput = self.NodeCodeAtInput(1)

        setCode = f"""
{self.name}={setInput}
{brotherCode}"""

        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{BooleanColor};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{setCode}</span></p></pre> """

        return code


@set_var_ID(VAR_STRING)
class StringVar(MasterNode):
    icon = ""
    node_type = VAR_STRING
    name = "string"
    content_label_objname = "var_node_string"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[4])
        self.isVar = True
        self.grNode._brush_title = QBrush(QColor(StringColor))

    def toGetter(self):
        self.isSetter = False
        self.initSockets(inputs=[], outputs=[4])
        self.getNodeCode = self.getterCode

    def toSetter(self):
        self.isSetter = True
        self.initSockets(inputs=[0, 4], outputs=[0])
        self.getNodeCode = self.setterCode

    def getterCode(self):
        self.showCode = False
        getCode = self.name
        return getCode

    def setterCode(self):
        self.showCode = not self.isInputConnected(0)
        brotherCode = self.NodeCodeAtOutput(0)
        setInput = self.NodeCodeAtInput(1)

        setCode = f"""
{self.name}={setInput}
{brotherCode}"""

        if self.isSelected() is True:
            colorStyle = f''' style=" Font-size:{FontSize}px ; background-color:{StringColor};" '''
        else:
            colorStyle = f''' style=" Font-size:{FontSize}px ;" '''

        code = f""" <pre><p style="font-family: {FontFamily} "><span {colorStyle} >{setCode}</span></p></pre> """

        return code
