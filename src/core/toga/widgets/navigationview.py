from .base import Widget


class NavigationView(Widget):
    def __init__(self, root_widget, id=None, style=None, factory=None, bar_button_item=None):
        super().__init__(id=id, style=style, factory=factory)
        self._impl = self.factory.NavigationView(root_widget._impl,
                                                 interface=self, bar_button_item=bar_button_item)

    def push(self, widget, animated=True, back_button=True):
        widget.app = self.app
        widget.window = self.window
        self._impl.push(widget._impl, animated, back_button=back_button)
        widget.refresh()

    def refresh(self):
        # TODO: Refresh child when popped?
        self._impl.refresh()

    def add(self, *children):
        name = self.__class__.__name__
        raise RuntimeError(f'Use push to add content to {name}')
