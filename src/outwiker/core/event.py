# -*- coding: UTF-8 -*-

EVENT_PRIORITY_DEFAULT = 0
EVENT_PRIORITY_MAX_CORE = 100
EVENT_PRIORITY_MIN_CORE = -100


class Event (object):
    """
    Events with priority
    """
    def __init__ (self):
        # List of the tuples: (event handler, priority)
        # First item - handler with max priority
        self._handlers = []


    def clear (self):
        del self._handlers[:]


    def bind (self, handler, priority=EVENT_PRIORITY_DEFAULT):
        for item in self._handlers:
            if item[0] == handler:
                return

        # Find last handler with priority less current priority
        index = 0
        for n, item in reversed(list(enumerate(self._handlers))):
            if item[1] >= priority:
                index = n + 1
                break

        self._handlers.insert (index, (handler, priority))


    def __iadd__ (self, handler):
        self.bind (handler)
        return self


    def __isub__ (self, handler):
        removed_item = None
        for item in self._handlers:
            if item[0] == handler:
                removed_item = item
                break

        if removed_item is None:
            raise ValueError("Handler is not handling this event, so cannot unhandle it.")

        self._handlers.remove (removed_item)
        return self


    def __call__ (self, *args, **kargs):
        for handler in self._handlers:
            handler[0](*args, **kargs)


    def __len__ (self):
        return len (self._handlers)
