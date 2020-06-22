from .base import Widget


class NavigationView(Widget):
    def __init__(self, root_widget, id=None, style=None, factory=None, bar_button_item=None):
        super().__init__(id=id, style=style, factory=factory)
        self._impl = self.factory.NavigationView(root_widget._impl,
                                                 interface=self, bar_button_item=bar_button_item)

    def push(self, widget, animated=True, right_bar_button_item=None, back_button=True):
        widget.app = self.app
        widget.window = self.window
        self._impl.push(widget._impl, animated, right_bar_button_item=right_bar_button_item, back_button=back_button)
        widget.refresh()

    def refresh(self):
        # TODO: Refresh child when popped?
        self._impl.refresh()
        pass

    def add(self, *children):
        name = self.__class__.__name__
        raise RuntimeError(f'Use push to add content to {name}')

    def back(self):
        self._impl.back()

    def set_parent_title(self, value):
        self._impl.set_parent_title(value)

    @property
    def title(self):
        return self._impl.title

    @title.setter
    def title(self, value):
        self._impl.title = value
