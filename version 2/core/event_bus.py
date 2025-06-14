class EventBus:
    def __init__(self):
        self.listeners = {}

    def on(self, event_type, handler):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(handler)

    def emit(self, event_type, **kwargs):
        for handler in self.listeners.get(event_type, []):
            handler(**kwargs)

event_bus = EventBus()
