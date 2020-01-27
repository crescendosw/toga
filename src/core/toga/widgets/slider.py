from toga.handlers import wrapped_handler

from .base import Widget


class Slider(Widget):
    """ Slider widget, displays a range of values

    Args:
        id: An identifier for this widget.
        style (:obj:`Style`):
        default (float): Default value of the slider
        range (``tuple``): Min and max values of the slider in this form (min, max).
        on_slide (``callable``): The function that is executed on_slide.
        enabled (bool): Whether user interaction is possible or not.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
    """
    MIN_WIDTH = 100

    def __init__(self, id=None, style=None, default=None, range=None, on_slide=None, enabled=True, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self._on_slide = None # needed for _impl initialization
        self._impl = self.factory.Slider(interface=self)

        self.range = range
        if default:
            self.value = default
        self.on_slide = on_slide
        self.enabled = enabled

    @property
    def value(self):
        return self._impl.get_value()

    @value.setter
    def value(self, value):
        min, max = self.range
        if not (min <= value <= max):
            raise ValueError('Slider value ({}) is not in range ({}-{})'.format(value, min, max))
        self._impl.set_value(value)

    @property
    def range(self):
        """ Range composed of min and max slider value.

        Returns:
            Returns the range in a ``tuple`` like this (min, max)
        """
        return self._range

    @range.setter
    def range(self, range):
        default_range = (0.0, 1.0)
        _min, _max = default_range if range is None else range
        if _min > _max or _min == _max:
            raise ValueError('Range min value has to be smaller than max value.')
        self._range = (_min, _max)
        self._impl.set_range((_min, _max))

    @property
    def on_slide(self):
        """ The function for when the slider is slided

        Returns:
            The ``callable`` that is executed on slide.
        """
        return self._on_slide

    @on_slide.setter
    def on_slide(self, handler):
        self._on_slide = wrapped_handler(self, handler)
        self._impl.set_on_slide(self._on_slide)

    @property
    def continuous(self):
        """ A Boolean indicating whether sliding the slider generates continuous update events.

        Returns:
            (bool) True if enabled, False if disabled.
        """
        return self._impl.continuous

    @continuous.setter
    def continuous(self, continuous):
        self._impl.continuous = continuous
