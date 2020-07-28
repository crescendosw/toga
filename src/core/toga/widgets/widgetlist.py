from .base import Widget


class WidgetList(Widget):
    MIN_WIDTH = 100
    MIN_HEIGHT = 100

    def __init__(self, headings, id=None, style=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self.headings = headings
        self.rows_added = 0

        self._impl = self.factory.WidgetList(interface=self)
