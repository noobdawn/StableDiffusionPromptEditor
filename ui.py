from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from graphics_scene import QDMGraphicsScene
from graphics_view import QDMGraphicsView
from node import PromptNode
from event import events
from system import PromptEditor

class NodeEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        events.add_event(events.EVENT_TYPE_ADD_NODE, self.on_add_node)
        events.add_event(events.EVENT_TYPE_DEL_NODE, self.on_del_node)
        events.add_event(events.EVENT_TYPE_NODE_SELECTED, self.on_node_selected)

        self.initUI()
        self.setWindowTitle("Stable Diffision Prompt Editor")

    def initUI(self):
        self.setWindowTitle("Node Editor")

        self.scene = QDMGraphicsScene()
        self.view = QDMGraphicsView(self)
        self.view.setScene(self.scene)

        # 当前节点的属性
        self.prompt_label = QLabel("Prompt:")
        self.mean_label = QLabel("作用:")
        self.weight_label = QLabel("权重:")
        self.tag_label = QLabel("Tag:")
        self.weight_slider = QSlider(Qt.Horizontal)
        self.weight_slider.setMinimum(30)
        self.weight_slider.setMaximum(300)
        self.weight_slider.setValue(100)
        self.weight_slider.valueChanged.connect(self.on_weight_changed)
        self.tab_properties_widget = QTabWidget()
        self.tab_properties_widget.setMinimumWidth(300)
        self.tab_properties_widget.setMaximumHeight(150)
        self.tab1_layout = QVBoxLayout()
        self.tab1_layout.addWidget(self.prompt_label)
        self.tab1_layout.addWidget(self.tag_label)
        self.tab1_layout.addWidget(self.mean_label)
        self.tab1_layout.addWidget(self.weight_label)
        self.tab1_layout.addWidget(self.weight_slider)
        self.tab1 = QWidget()
        self.tab1.setLayout(self.tab1_layout)
        self.tab_properties_widget.addTab(self.tab1, "Properties")
        
        # 添加节点
        self.filter_combo = QComboBox()
        filters = PromptEditor.instance()._tags.keys()
        for filter in filters:
            self.filter_combo.addItem(filter)
        self.filter_combo.currentTextChanged.connect(self.on_filter_changed)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.grid_layout = QGridLayout()
        self.grid_layout.setAlignment(Qt.AlignTop)
        self.grid_layout.setSpacing(10)
        self.prompt_btns = []
        idx = 0
        for filterName, filterDic in PromptEditor.instance()._tags.items():
            for prompt, meaning in filterDic["EtoZ"].items():
                btn = QPushButton(meaning)
                btn.prompt = prompt
                btn.meaning = meaning
                btn.filter = filterName
                btn.isadd = filterDic["add"]
                btn.pen = filterDic["pen"]
                btn.brush = filterDic["brush"]
                btn.clicked.connect(self.on_click_add)
                self.prompt_btns.append(btn)
                self.grid_layout.addWidget(btn, idx // 2, idx % 2)
                idx += 1
        self.scroll_area.setLayout(self.grid_layout)

        self.tab_add_widget = QTabWidget()
        self.tab_add_widget.setMinimumWidth(300)
        self.tab_add_widget.setMinimumHeight(450)
        self.tab2_layout = QVBoxLayout()
        self.tab2_layout.addWidget(self.filter_combo)
        self.tab2_layout.addWidget(self.scroll_area)
        self.tab2 = QWidget()
        self.tab2.setLayout(self.tab2_layout)
        self.tab_add_widget.addTab(self.tab2, "Add Prompt")

        # 输出部分
        self.label_positive = QLabel("Positive Prompt")
        self.positive_edit = QTextEdit()
        self.label_negative = QLabel("Negative Prompt")
        self.negative_edit = QTextEdit()
        self.update_btn = QPushButton("输出")
        self.update_btn.clicked.connect(self.on_click_update)
        self.output_tab_widget = QTabWidget()
        self.output_tab_widget.setMinimumWidth(300)
        self.output_tab1_layout = QVBoxLayout()
        self.output_tab1_layout.addWidget(self.label_positive)
        self.output_tab1_layout.addWidget(self.positive_edit)
        self.output_tab1_layout.addWidget(self.label_negative)
        self.output_tab1_layout.addWidget(self.negative_edit)
        self.output_tab1_layout.addWidget(self.update_btn)
        self.output_tab1 = QWidget()
        self.output_tab1.setLayout(self.output_tab1_layout)
        self.output_tab_widget.addTab(self.output_tab1, "Output")

        rightVBox = QVBoxLayout()
        rightVBox.addWidget(self.tab_properties_widget)
        rightVBox.addWidget(self.tab_add_widget)
        rightVBox.addWidget(self.output_tab_widget)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.view)
        mainLayout.addLayout(rightVBox)

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        self.filter_combo.setCurrentIndex(0)
        self.on_filter_changed(self.filter_combo.currentText())

        self.show()

    def on_weight_changed(self, value):
        events.trigger_event(events.EVENT_TYPE_UI_WEIGHT_CHANGED, value / 100.0)

    def on_filter_changed(self, text):
        for btn in self.prompt_btns:
            if btn.filter == text:
                btn.show()
            else:
                btn.hide()

    def on_click_add(self):
        btn = self.sender()
        node = PromptNode(btn.prompt, btn.meaning, btn.filter, btn.isadd, 1)
        node.setPen(btn.pen)
        node.setBrush(btn.brush)
        events.trigger_event(events.EVENT_TYPE_ADD_NODE, node)

    def on_click_update(self):
        nodes = PromptEditor.instance()._nodes.copy()
        if (len(nodes) == 0):
            return
        nodes.sort(key=lambda x: x.position().x(), reverse=False)
        positive = ""
        negative = ""
        for node in nodes:
            text = node.prompt
            if node.weight != 1:
                text = f"({text} : {node.weight})"
            if node.isAdd:
                positive = positive + text + ", "
            else:
                negative = negative + text + ", "
        self.positive_edit.setText(positive)
        self.negative_edit.setText(negative)

    def on_add_node(self, node):
        self.scene.addItem(node.get_graphics_node())

    def on_del_node(self, node):
        self.scene.removeItem(node.get_graphics_node())

    def on_node_selected(self, node):
        self.prompt_label.setText("Prompt:" + node.prompt)
        self.mean_label.setText("作用:" + node.meaning)
        self.weight_label.setText("权重:" + str(node.weight))
        self.tag_label.setText("Tag:" + node.filter)
        self.weight_slider.setValue(int(node.weight * 100))

if __name__ == "__main__":
    PromptEditor.instance().loadTags()
    import sys
    app = QApplication(sys.argv)
    window = NodeEditorWindow()
    sys.exit(app.exec_())
