from collections import deque

class Memory:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.events = deque(maxlen=capacity)

    def add(self, event_type, location):
        self.events.append({"type": event_type, "location": location})

    def get(self, event_type=None):
        if event_type:
            return [e for e in self.events if e["type"] == event_type]
        return list(self.events)
