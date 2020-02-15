from ..libs import UINavigationController
from ..libs import UIView
from ..libs import NSNotificationCenter
from .base import Widget


class NavigationView(Widget):
    def __init__(self, root_widget, interface):
        super().__init__(interface, is_root_controller=True)
        if not root_widget or not isinstance(root_widget.native, UIView):
            name = self.__class__.__name__
            raise RuntimeError(f'Invalid root_widget for {name}')
        self.root_widget = root_widget

    def create(self):
        self.native = UINavigationController.alloc().init()
        self.native.interface = self.interface

    def on_set_content(self):
        self.interface.push(self.root_widget.interface, animated=False)

    def push(self, widget, animated):
        if not self.interface.window:
            name = self.__class__.__name__
            raise RuntimeError(f'Window content must be set to {name} '
                               f'instance before calling push')

        widget.constraints = None
        widget.native.translatesAutoresizingMaskIntoConstraints = True

        view_controller = self.interface.window._impl.configure_content(widget)
        view_controller.title = getattr(widget.interface, 'title', '')

        self.native.pushViewController_animated_(view_controller, animated)

    def refresh(self):
        pass

    # TODO: What is '_impl.rehint'?
    #      - toga.Button.rehint indicates that it has to do with resizing
    #      - Sets self.interface.intrinsic.width
    #      - The iOS _impl uses a viewport to add some vertical padding!!!
    #      - *** How to determine the size of the top & bottom navigation controller elements?
    #      - toga_iOS.ScrollContainer.constrain_to_scrollview, called by set_content, chops out various borders
    #        - toga_iOS.ScrollContainer.update_content_size calls self.native.setContentSize_ to chop out borders
    #      >>>>> What is an iOS container that chops out part of the UI
    #        - the iOS Window chops out room for the keyboard & status bar
    #        - the iOSViewport is what chops out the space - WHAT IS A VIEWPORT?
    #        - The iOSViewport is also used by the ScrollContainer
    # def rehint(self):
    #     self.update_content_size()
