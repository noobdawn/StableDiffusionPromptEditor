from color import EditorColor as cl
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class EditorLayout:
    CircleNodeRaidus = 100
    NodeSelectedEdgeWidth = 3
    NodeEdgeWidth = 2


    PenSelected = QPen(cl.NodeSelected, NodeSelectedEdgeWidth)
