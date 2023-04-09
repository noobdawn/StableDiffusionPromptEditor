from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from event import events

class QDMGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 设置渲染模式
        self.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform | QPainter.HighQualityAntialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.mouseDown = False
        self.lastMousePos = None

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.RightButton:
            self.mouseDown = True
            self.lastMousePos = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self.mouseDown:
            delta = event.pos() - self.lastMousePos
            self.lastMousePos = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.RightButton:
            self.mouseDown = False
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event) -> None:
        if event.angleDelta().y() > 0:
            factor = 1.25
        else:
            factor = 0.8
        self.scale(factor, factor)

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Delete:
            events.trigger_event(events.EVENT_TYPE_UI_DEL_NODE)
        return super().keyPressEvent(event)