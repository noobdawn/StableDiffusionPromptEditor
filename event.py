class Event:
    def __init__(self):
        self.__handlers = []

    def add_handler(self, handler):
        self.__handlers.append(handler)

    def del_handler(self, handler):
        self.__handlers.remove(handler)

    def trigger(self, *args, **kwargs):
        for handler in self.__handlers:
            handler(*args, **kwargs)

class EventManager:
    EVENT_TYPE_NODE_SELECTED = 'node_selected'
    EVENT_TYPE_ADD_NODE = 'add_node'
    EVENT_TYPE_UI_WEIGHT_CHANGED = 'ui_weight_changed'
    EVENT_TYPE_WEIGHT_CHANGED = 'weight_changed'
    EVENT_TYPE_UI_DEL_NODE = 'ui_del_node'
    EVENT_TYPE_DEL_NODE = 'del_node'

    def __init__(self):
        self.__events = {}
        self.__events['default'] = Event()

    def add_event(self, event_name, callback = None):
        if event_name not in self.__events:
            self.__events[event_name] = Event()
        if callback is not None:
            self.__events[event_name].add_handler(callback)

    def del_event(self, event_name):
        if event_name in self.__events:
            del self.__events[event_name]

    def get_event(self, event_name):
        if event_name in self.__events:
            return self.__events[event_name]
        else:
            return self.__events['default']

    def trigger_event(self, event_name, *args, **kwargs):
        if event_name in self.__events:
            self.__events[event_name].trigger(*args, **kwargs)
        else:
            self.__events['default'].trigger(*args, **kwargs)

events = EventManager()


