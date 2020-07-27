from toga.handlers import wrapped_handler
from toga.sources import ListSource
from toga.sources.accessors import build_accessors

from .base import Widget


class WidgetList(Widget):
    MIN_WIDTH = 100
    MIN_HEIGHT = 100

    def __init__(self, headings, id=None, style=None, data=None, accessors=None,
                 multiple_select=False, on_select=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self.headings = headings
        self._accessors = build_accessors(headings, accessors)
        self._multiple_select = multiple_select
        self._on_select = None
        self._selection = None
        self._data = None

        self._impl = self.factory.WidgetList(interface=self)
        self.data = data

        self.on_select = on_select

    @property
    def data(self):
        """ The data source of the widget. It accepts table data
        in the form of ``list``, ``tuple``, or :obj:`ListSource`

        Returns:
            Returns a (:obj:`ListSource`).
        """
        return self._data

    @data.setter
    def data(self, data):
        if data is None:
            self._data = ListSource(accessors=self._accessors, data=[])
        elif isinstance(data, (list, tuple)):
            self._data = ListSource(accessors=self._accessors, data=data)
        else:
            self._data = data

        self._data.add_listener(self._impl)
        self._impl.change_source(source=self._data)

    @property
    def multiple_select(self):
        """Does the table allow multiple rows to be selected?"""
        return self._multiple_select

    @property
    def selection(self):
        """The current selection of the table.

        A value of None indicates no selection.
        If the table allows multiple selection, returns a list of
        selected data nodes. Otherwise, returns a single data node.
        """
        return self._selection

    def scroll_to_top(self):
        """Scroll the view so that the top of the list (first row) is visible
        """
        self.scroll_to_row(0)

    def scroll_to_row(self, row):
        """Scroll the view so that the specified row index is visible.

        Args:
            row: The index of the row to make visible. Negative values refer
                 to the nth last row (-1 is the last row, -2 second last,
                 and so on)
        """
        if row >= 0:
            self._impl.scroll_to_row(row)
        else:
            self._impl.scroll_to_row(len(self.data) + row)

    def scroll_to_bottom(self):
        """Scroll the view so that the bottom of the list (last row) is visible
        """
        self.scroll_to_row(-1)

    @property
    def on_select(self):
        """ The callback function that is invoked when a row of the table is selected.
        The provided callback function has to accept two arguments table (``:obj:Table`)
        and row (``int`` or ``None``).

        Returns:
            (``callable``) The callback function.
        """
        return self._on_select

    @on_select.setter
    def on_select(self, handler):
        """
        Set the function to be executed on node selection

        :param handler:     callback function
        :type handler:      ``callable``
        """
        self._on_select = wrapped_handler(self, handler)
        self._impl.set_on_select(self._on_select)
