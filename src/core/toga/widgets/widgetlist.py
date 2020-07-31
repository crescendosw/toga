from .base import Widget


class WidgetList(Widget):
    MIN_WIDTH = 100
    MIN_HEIGHT = 100

    def __init__(self, data, checkmark=None, id=None, style=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self.data = data
        self.checkmark = checkmark
        self._impl = self.factory.WidgetList(interface=self)

    def reload_data(self):
        self._impl.reload_data()
