from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from color import EditorColor
import math

class QDMGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.gridSize = 20

        self._pen_light = QPen(EditorColor.Light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(EditorColor.Dark)
        self._pen_dark.setWidth(2)
        self._pen_bound = QPen(EditorColor.Bound)
        self._pen_bound.setWidth(4)

        self.setBackgroundBrush(EditorColor.Background)

        self.scene_width, self.scene_height = 3000, 900
        self.setSceneRect(-self.scene_width // 2, -self.scene_height // 2, self.scene_width, self.scene_height)


    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)

        lines_light, lines_dark = [], []

        for x in range(first_left, right, self.gridSize):
            if x % (self.gridSize * 5) == 0:
                lines_dark.append(QLine(x, top, x, bottom))
            else:
                lines_light.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.gridSize):
            if y % (self.gridSize * 5) == 0:
                lines_dark.append(QLine(left, y, right, y))
            else:
                lines_light.append(QLine(left, y, right, y))

        painter.setPen(self._pen_light)
        painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        painter.drawLines(*lines_dark)

        painter.setPen(self._pen_bound)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(QRectF(-self.scene_width // 2, -self.scene_height // 2, self.scene_width, self.scene_height))