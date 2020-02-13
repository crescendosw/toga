from toga_iOS import dialogs
from toga_iOS.libs import UIApplication, UIScreen, UIViewController, UIWindow
from rubicon.objc import objc_method


class iOSViewport:
    def __init__(self, view):
        self.view = view
        self.dpi = 96  # FIXME This is almost certainly wrong...

        self.kb_height = 0.0

    @property
    def statusbar_height(self):
        # This is the height of the status bar frame.
        # If the status bar isn't visible (e.g., on iPhones in landscape orientation)
        # the size will be 0.
        return UIApplication.sharedApplication.statusBarFrame.size.height

    @property
    def width(self):
        return self.view.bounds.size.width

    @property
    def height(self):
        # Remove the height of the keyboard and the titlebar
        # from the available viewport height
        return self.view.bounds.size.height - self.kb_height - self.statusbar_height


class Window:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.controller = None
        self.create()

    def create(self):
        self.native = UIWindow.alloc().initWithFrame(UIScreen.mainScreen.bounds)
        self.native.interface = self.interface

    def set_content(self, widget):
        if widget.is_root_controller:
            widget.on_set_content()
            self.controller = widget.native
            self.native.rootViewController = self.controller
        else:
            if getattr(widget, 'controller', None):
                view_controller = widget.controller
            else:
                view_controller = None

            self.controller = self.configure_content(widget, view_controller)
            self.native.rootViewController = self.controller

    def configure_content(self, widget, view_controller=None):
        widget.viewport = iOSViewport(self.native)
        if not view_controller:
            view_controller = ViewControllerWrapper.alloc().init()

        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

        view_controller._view_impl = widget # TODO: Hacky
        view_controller.view = widget.native

        return view_controller

    def set_title(self, title):
        pass

    def set_position(self, position):
        pass

    def set_size(self, size):
        pass

    def set_app(self, app):
        pass

    def create_toolbar(self):
        pass

    def show(self):
        self.native.makeKeyAndVisible()

        # Refresh with the actual viewport to do the proper rendering.
        self.interface.content.refresh()

    def info_dialog(self, title, message):
        return dialogs.info_dialog(self.interface, title, message)

    def question_dialog(self, title, message):
        return dialogs.question_dialog(self.interface, title, message)

    def confirm_dialog(self, title, message):
        return dialogs.confirm_dialog(self.interface, title, message)

    def error_dialog(self, title, message):
        return dialogs.error_dialog(self.interface, title, message)

    def stack_trace_dialog(self, title, message, content, retry=False):
        self.interface.factory.not_implemented('Window.stack_trace_dialog()')


class ViewControllerWrapper(UIViewController):
    @objc_method
    def willMoveToParentViewController_(self, parent) -> None:
        # TODO: We should be calling the super class here
        # super(self.__class__, self.__class__).willMoveToParentViewController_(parent)
        if not parent:
            on_close = getattr(self._view_impl.interface, 'on_close', None)
            if on_close:
                on_close()
