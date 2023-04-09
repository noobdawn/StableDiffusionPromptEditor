from event import events
from color import EditorColor as ec

class PromptEditor:
    _instance = None
    _current_node = None
    _nodes = []
    _tags = {}

    def __init__(self):
        events.add_event(events.EVENT_TYPE_NODE_SELECTED, self.node_selected)
        events.add_event(events.EVENT_TYPE_ADD_NODE, self.add_node)
        events.add_event(events.EVENT_TYPE_UI_WEIGHT_CHANGED, self.on_ui_weight_changed)
        events.add_event(events.EVENT_TYPE_UI_DEL_NODE, self.del_node)

    @staticmethod
    def instance():
        if PromptEditor._instance is None:
            PromptEditor._instance = PromptEditor()
        return PromptEditor._instance

    def node_selected(self, node):
        self._current_node = node

    def add_node(self, node):
        self._nodes.append(node)
        if (len(self._nodes) == 1):
            events.trigger_event(events.EVENT_TYPE_NODE_SELECTED, node)

    def del_node(self):
        if self._current_node is not None:
            events.trigger_event(events.EVENT_TYPE_DEL_NODE, self._current_node)
            self._nodes.remove(self._current_node)
            if (len(self._nodes) > 0):
                events.trigger_event(events.EVENT_TYPE_NODE_SELECTED, self._nodes[0])
            else:
                self._current_node = None

    def on_ui_weight_changed(self, weight):
        if self._current_node is not None:
            events.trigger_event(events.EVENT_TYPE_WEIGHT_CHANGED, self._current_node, weight)
            events.trigger_event(events.EVENT_TYPE_NODE_SELECTED, self._current_node)

    def loadTags(self):
        import os
        folder = os.path.dirname(os.path.abspath(__file__))
        for filename in os.listdir(folder):
            print(filename)
            if filename.endswith(".tags"):
                filterName = filename[:-5]
                filterDic = {}
                ZtoE = {}
                EtoZ = {}
                brushColor = "#000000"
                with open(filename, 'r') as f:
                    lines = f.readlines()
                    brushColor = lines[0].strip()
                    for line in lines[1:]:
                        meaning, prompt = line.strip().split('::::', 1)
                        ZtoE[meaning] = prompt
                        EtoZ[prompt] = meaning
                filterDic["ZtoE"] = ZtoE
                filterDic["EtoZ"] = EtoZ
                filterDic["brush"] = brushColor
                # 针对正面和负面的各增加一个标签
                filterDic['pen'] = ec.EdgePositive
                filterDic['add'] = True
                self._tags[filterName + '+'] = filterDic.copy()
                filterDic['pen'] = ec.EdgeNegative
                filterDic['add'] = False
                self._tags[filterName + '-'] = filterDic
        print(self._tags)

