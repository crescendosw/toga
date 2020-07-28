from .base import Widget


class WidgetList(Widget):
    MIN_WIDTH = 100
    MIN_HEIGHT = 100

    def __init__(self, labels, widgets, id=None, style=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self.lables = labels
        self._impl = self.factory.WidgetList(interface=self)
