from ..libs import UINavigationController
from ..libs import UIView
from ..libs import NSNotificationCenter
from .base import Widget
from ..window import iOSViewport
from toga_iOS.libs import UIScreen


class NavigationView(Widget):
    def __init__(self, root_widget, interface, bar_button_item=None):
        # self.set_bounds(UIScreen.mainScreen.bounds.origin.x,
        #                 UIScreen.mainScreen.bounds.origin.y,
        #                 UIScreen.mainScreen.bounds.size.width,
        #                 UIScreen.mainScreen.bounds.size.height)
        # self.viewport = iOSViewport(self)#type('', (), {'kb_height': 100})
        self.bar_button_item = bar_button_item
        super().__init__(interface, is_root_controller=True)
        if not root_widget or not isinstance(root_widget.native, UIView):
            name = self.__class__.__name__
            raise RuntimeError(f'Invalid root_widget for {name}')
        self.root_widget = root_widget
        self._view_controllers = [self.root_widget]

    def create(self):
        self.native = UINavigationController.alloc().init()
        self.native.interface = self.interface

    def on_set_content(self):
        self.interface.push(self.root_widget.interface, animated=False, back_button=False)

    def push(self, widget, animated, back_button=True):
        if not self.interface.window:
            name = self.__class__.__name__
            raise RuntimeError(f'Window content must be set to {name} '
                               f'instance before calling push')

        widget.constraints = None
        widget.native.translatesAutoresizingMaskIntoConstraints = True

        view_controller = self.interface.window._impl.configure_content(widget)
        view_controller.title = getattr(widget.interface, 'title', '')
        if self.bar_button_item and not back_button:
            view_controller.navigationItem.leftBarButtonItem = self.bar_button_item
        view_controller.nav_view = self

        self.native.pushViewController_animated_(view_controller, animated)
        self._view_controllers.append(widget)

    def on_back(self, view_controller):
        assert self._view_controllers.pop() == view_controller
        self._view_controllers.pop()


    def refresh(self):
        for view in self._view_controllers:
            view.interface.refresh()

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
