from toga.handlers import wrapped_handler

from .base import Widget


class BarButtonItem(Widget):
    """A clickable button widget.

    Args:
        label (str): Text to be shown on the button.
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        on_press (:obj:`callable`): Function to execute when pressed.
        enabled (bool): Whether or not interaction with the button is possible, defaults to `True`.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
    """

    def __init__(self, image, id=None, on_press=None, factory=None):
        self.image = image
        #self.on_press = on_press
        super().__init__(id=id, enabled=True, style=None, factory=factory)

        # Create a platform specific implementation of a Button
        self._impl = self.factory.BarButtonItem(interface=self)
        self.on_press = on_press

    @property
    def label(self):
        """
        Returns:
            The button label as a ``str``
        """
        return self._label

    @label.setter
    def label(self, value):
        if value is None:
            self._label = ''
        else:
            self._label = str(value)
        self._impl.set_label(value)
        self._impl.rehint()

    # @property
    # def image(self):
    #     return 'yeet'
    #
    # @image.setter
    # def image(self, value):
    #     self._image = value
    #     if value:
    #         value.bind(self.factory)
    #         self._impl.set_image(value._impl)
    #     self._impl.rehint()


    @property
    def on_press(self):
        """The handler to invoke when the button is pressed.

        Returns:
            The function ``callable`` that is called on button press.
        """
        return self._on_press

    @on_press.setter
    def on_press(self, handler):
        """Set the handler to invoke when the button is pressed.

        Args:
            handler (:obj:`callable`): The handler to invoke when the button is pressed.
        """
        self._on_press = wrapped_handler(self, handler)
        self._impl.set_on_press(self._on_press)
