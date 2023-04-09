from graphics_node import QDMCircleGraphicsNode
from event import events
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class PromptNode:
    def __init__(self, prompt, meaning, filter, positive : bool = True, weight : float = 1):
        self.prompt = prompt
        self.meaning = meaning
        self.isAdd = positive
        self.weight = weight
        self.filter = filter
        self.gnode = QDMCircleGraphicsNode(self.prompt, self.isAdd, self.weight, self)
        events.add_event(events.EVENT_TYPE_NODE_SELECTED, self.on_node_selected)
        events.add_event(events.EVENT_TYPE_WEIGHT_CHANGED, self.on_weight_changed)

    def get_graphics_node(self):
        return self.gnode
    
    def set_prompt(self, prompt):
        self.prompt = prompt
        self.gnode.title = prompt

    def set_weight(self, weight):
        self.weight = weight
        self.gnode.weight = weight

    def select_from_gnode(self):
        events.trigger_event(events.EVENT_TYPE_NODE_SELECTED, self)

    def on_node_selected(self, node):
        if node == self:
            self.gnode.isSelected = True
            self.gnode.update()
        else:
            self.gnode.isSelected = False
            self.gnode.update()

    def on_weight_changed(self, node, weight):
        if node == self:
            self.set_weight(weight)

    def setPen(self, code : str):
        self.gnode.setPen(QColor(code))
        self.gnode.update()

    def setBrush(self, code : str):
        self.gnode.setBrush(QColor(code))
        self.gnode.update()

    def position(self):
        return self.gnode.pos()