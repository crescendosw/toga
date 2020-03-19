from rubicon.objc import objc_method, CGSize, SEL
from travertino.size import at_least

from toga_iOS.libs import (
    UIBarButtonItem,
    UIColor,
    UIControlEventTouchDown,
    UIControlStateDisabled,
    UIControlStateNormal
)
from toga_iOS.widgets.base import Widget


class TogaBarButtonItem(UIBarButtonItem):
    @objc_method
    def onPress_(self, obj) -> None:
        if self.interface.on_press:
            self.interface.on_press(self.interface)


class BarButtonItem(Widget):
    def create(self):
        self.native = TogaBarButtonItem.alloc().initWithImage_style_target_action_(self.interface.image._impl.native, 0, self.native, SEL('onPress:'))
        self.native.interface = self.interface

        # Add the layout constraints
        self.add_constraints()

    def set_on_press(self, handler):
        # No special handling required.
        pass

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(fitting_size.width)
        self.interface.intrinsic.height = fitting_size.height
