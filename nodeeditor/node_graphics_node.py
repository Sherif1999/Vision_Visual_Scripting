# -*- coding: utf-8 -*-
"""
A module containing Graphics representation of :class:`~nodeeditor.node_node.Node`
"""
from qtpy.QtWidgets import QGraphicsItem, QWidget, QGraphicsTextItem, QGraphicsDropShadowEffect
from qtpy.QtGui import QFont, QColor, QPen, QBrush, QPainterPath
from qtpy.QtCore import Qt, QRectF


class QDMGraphicsNode(QGraphicsItem):
    """Class describing Graphics representation of :class:`~nodeeditor.node_node.Node`"""

    def __init__(self, node: 'Node', parent: QWidget = None):
        """
        :param node: reference to :class:`~nodeeditor.node_node.Node`
        :type node: :class:`~nodeeditor.node_node.Node`
        :param parent: parent widget
        :type parent: QWidget

        :Instance Attributes:

            - **node** - reference to :class:`~nodeeditor.node_node.Node`
        """
        super().__init__(parent)
        self.node = node

        # init our flags
        self.hovered = False
        self._was_moved = False
        self._last_selected_state = False

        self.updateSizes()
        self.initAssets()
        self.initUI()

        # creating a QGraphicsDropShadowEffect object
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(14, 14, 14))

        shadow.setXOffset(-6)
        shadow.setYOffset(6)
        # setting blur radius (optional step)
        shadow.setBlurRadius(12)
        # adding shadow to the grNode
        self.setGraphicsEffect(shadow)

    @property
    def content(self):
        """Reference to `Node Content`"""
        return self.node.content if self.node else None

    @property
    def name(self):
        """title of this `Node`

        :getter: current Graphics Node title
        :setter: stores and make visible the new title
        :type: str
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.grName = self._name

        self.name_item.setPlainText(self.grName)
        self.name_item.adjustSize()

        if self.name_item.textWidth()+40 > self.width:
            while self.name_item.textWidth()+40 > self.width:
                self.grName = self.grName[0: -1]
                self.name_item.setPlainText(self.grName)
                self.name_item.adjustSize()

            self.name_item.setPlainText(self.grName+"...")
            self.name_item.adjustSize()

    def initUI(self):
        """Set up this ``QGraphicsItem``"""
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

        # init title
        self.initName()
        self.name = self.node.name

        # self.initContent()

    def updateSizes(self):
        """Set up internal attributes like `width`, `height`, etc."""
        self.width = 180
        self.height = 80
        self.edge_roundnes = 2
        self.edge_padding = 0
        self.title_height = 30
        self.title_horizontal_padding = 24
        self.title_vertical_padding = 10


    def AutoResizeGrNode(self):
        socketsHeight = self.title_height
        if len(self.node.inputs) > len(self.node.outputs):
            maxSockets = self.node.inputs
        else:
            maxSockets = self.node.outputs

        for socket in maxSockets:
            socketsHeight += self.node.socket_spacing

        self.height = socketsHeight

    def initAssets(self):
        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""
        self._title_color = Qt.white
        self._title_font = QFont("Roboto", 14)

        self._color = QColor("#FF000000")
        self._color_selected = QColor("#FFFFA637")
        self._color_hovered = QColor("#FFFFFF")

        self._pen_default = QPen(self._color)
        self._pen_default.setWidthF(1.5)
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidthF(2.0)
        self._pen_hovered = QPen(self._color_hovered)
        self._pen_hovered.setWidthF(1)

        self.node_color = QColor("#FF313131")
        self._brush_title = QBrush(self.node_color)
        self._brush_background = QBrush(QColor("#FF212121"))

    def onSelected(self):
        """Our event handling when the node was selected"""
        self.node.scene.grScene.itemSelected.emit()


    def doSelect(self, new_state=True):
        """Safe version of selecting the `Graphics Node`. Takes care about the selection state flag used internally

        :param new_state: ``True`` to select, ``False`` to deselect
        :type new_state: ``bool``
        """
        self.setSelected(new_state)
        self._last_selected_state = new_state
        if new_state: self.onSelected()

    def mouseMoveEvent(self, event):
        """Overridden event to detect that we moved with this `Node`"""
        super().mouseMoveEvent(event)

        # optimize me! just update the selected nodes
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()
        self._was_moved = True

    def mouseReleaseEvent(self, event):
        """Overriden event to handle when we moved, selected or deselected this `Node`"""
        super().mouseReleaseEvent(event)

        # handle when grNode moved
        if self._was_moved:
            self._was_moved = False
            self.node.scene.history.storeHistory("Node moved", setModified=True)

            self.node.scene.resetLastSelectedStates()
            self.doSelect()  # also trigger itemSelected when node was moved

            # we need to store the last selected state, because moving does also select the nodes
            self.node.scene._last_selected_items = self.node.scene.getSelectedItems()

            # now we want to skip storing selection
            return

        # handle when grNode was clicked on
        if self._last_selected_state != self.isSelected() or self.node.scene._last_selected_items != self.node.scene.getSelectedItems():
            self.node.scene.resetLastSelectedStates()
            self._last_selected_state = self.isSelected()
            self.onSelected()

    def mouseDoubleClickEvent(self, event):
        """Overriden event for doubleclick. Resend to `Node::onDoubleClicked`"""
        self.node.onDoubleClicked(event)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        """Handle hover effect"""
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        """Handle hover effect"""
        self.hovered = False
        self.update()

    def boundingRect(self) -> QRectF:
        """Defining Qt' bounding rectangle"""
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()

    def initName(self):
        """Set up the title Graphics representation: font, color, position, etc."""
        self.name_item = QGraphicsTextItem(self)
        # self.name_item
        self.name_item.node = self.node
        self.name_item.setDefaultTextColor(self._title_color)
        self.name_item.setFont(self._title_font)
        self.name_item.setPos(self.title_horizontal_padding, 0)
        # self.name_item.setTextWidth(self.width - 2 * self.title_horizontal_padding)

    def initContent(self):
        """Set up the `grContent` - ``QGraphicsProxyWidget`` to have a container for `Graphics Content`"""
        if self.content is not None:
            self.content.setGeometry(self.edge_padding, self.title_height + self.edge_padding,
                                     self.width - 2 * self.edge_padding,
                                     self.height - 2 * self.edge_padding - self.title_height)

        # get the QGraphicsProxyWidget when inserted into the grScene
        self.grContent = self.node.scene.grScene.addWidget(self.content)
        self.grContent.node = self.node
        self.grContent.setParentItem(self)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Painting the rounded rectanglar `Node`"""
        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, 0, self.width, self.height, self.edge_roundnes, self.edge_roundnes)
        path_content.addRect(0, self.title_height, self.edge_roundnes, self.edge_roundnes)
        path_content.addRect(self.width - self.edge_roundnes, self.title_height, self.edge_roundnes,
                             self.edge_roundnes)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_roundnes, self.edge_roundnes)
        path_title.addRect(0, self.title_height - self.edge_roundnes, self.edge_roundnes, self.edge_roundnes)
        path_title.addRect(self.width - self.edge_roundnes, self.title_height - self.edge_roundnes,
                           self.edge_roundnes, self.edge_roundnes)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(-1, -1, self.width + 2, self.height + 2, self.edge_roundnes, self.edge_roundnes)
        painter.setBrush(Qt.NoBrush)

        if self.hovered:
            painter.setBrush(QColor("#10FFFFFF"))
            painter.setPen(self._pen_hovered)
            painter.drawPath(path_outline.simplified())
            # painter.setPen(self._pen_default)
            painter.drawPath(path_outline.simplified())
        else:
            painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
            painter.drawPath(path_outline.simplified())

