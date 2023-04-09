from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from layout import EditorLayout as el
from color import EditorColor as cl


class QDMCircleGraphicsNode(QGraphicsItem):
    def __init__(self, title : str, add : bool, weight : float, receiver, parent=None):
        super(QDMCircleGraphicsNode, self).__init__(parent)
        self.title = title
        self.isSelected = False
        self.isAdd = add
        self.weight = weight
        self.radius = el.CircleNodeRaidus * self.weight
        self.receiver = receiver
        self.pen = QPen(cl.Light, el.NodeEdgeWidth)
        self.brush = QBrush(cl.NodeBackground)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def boundingRect(self):
        return QRectF(-self.radius, -self.radius, self.radius, self.radius)

    def paint(self, painter, option, widget):        
        # 绘制选中状态下的圆圈
        if (self.isSelected):
            path_outline = QPainterPath()
            rect = self.boundingRect()
            rect.adjust(-el.NodeEdgeWidth * 2, -el.NodeEdgeWidth * 2, el.NodeEdgeWidth * 2, el.NodeEdgeWidth * 2)
            path_outline.addEllipse(rect)
            painter.setPen(el.PenSelected)
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(path_outline.simplified())

        # 绘制边框和背景
        rect = self.boundingRect()
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawEllipse(rect)

        # 绘制标题
        font = QFont("Arial", 10 * self.weight, QFont.Bold)
        painter.setPen(cl.NodeTitle)
        painter.setFont(font)
        rect.adjust(0, -5 * self.weight, 0, -5 * self.weight)
        painter.drawText(self.boundingRect(), Qt.AlignCenter, self.title)

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        self._title = title
        self.update()

    @property
    def weight(self):
        return self._weight
    
    @weight.setter
    def weight(self, weight):
        self._weight = weight
        self.radius = el.CircleNodeRaidus * self.weight
        self.update()

    def mousePressEvent(self, event):
        self.receiver.select_from_gnode()
        self.update()
        super().mousePressEvent(event)

    def setPen(self, code : str):
        self.pen = QPen(code, el.NodeEdgeWidth)
        self.update()

    def setBrush(self, code : str):
        self.brush = QBrush(code)
        self.update()