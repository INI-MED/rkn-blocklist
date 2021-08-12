import logging


class EmitterClass:

    listeners = {}

    def on(self, event: str, listener):
        listeners = self.listeners.get(event)
        if not listeners:
            new_set = set()
            new_set.add(listener)
            self.listeners[event] = new_set
        else:
            listeners.add(listener)

    def off(self, event: str, listener):
        listeners = self.listeners.get(event)
        if listeners:
            listeners.remove(listener)

    def emit(self, event: str):
        logging.info(f"Emitted event {event}")
        listeners = self.listeners.get(event)
        if listeners:
            for listener in listeners:
                listener()

