from travertino.size import at_least

from toga_iOS.libs import *
from .base import Widget
from rubicon.objc import SEL


class Switch(UISwitch):
    @objc_method
    def onPress_(self, obj) -> None:
        if self.on_press:
            self.on_press(obj.isOn())


class TogaWidgetList(UITableView):
    @objc_method
    def tableView_numberOfRowsInSection_(self, table) -> int:
        return len(table.interface.data)

    @objc_method
    def numberOfSectionsInTableView_(self) -> int:
        return 1

    @objc_method
    def tableView_cellForRowAtIndexPath_(self, table, index_path) -> type(UITableViewCell):
        cell_identifier = 'cell identifier'
        cell = table.dequeueReusableCellWithIdentifier_(cell_identifier)
        if not cell:
            cell = UITableViewCell.alloc().initWithStyle_reuseIdentifier_(UITableViewCellStyleValue1, cell_identifier)
        cell.textLabel.text = table.interface.data[index_path.row]['title']
        if table.interface.checkmark is None:
            cell.detailTextLabel.text = table.interface.data[index_path.row]['label']
            accessory = table.interface.data[index_path.row]['widget']
            if accessory == 'switch':
                switch = Switch.alloc().initWithFrame_(CGRectMake(0, 0, 0, 0))
                switch.setOn(table.interface.data[index_path.row]['value'])
                switch.on_press = table.interface.data[index_path.row]['action']
                switch.addTarget(switch, action=SEL('onPress:'), forControlEvents=4096)
                cell.accessoryView = switch
            elif accessory == 'arrow':
                cell.accessoryType = UITableViewCellAccessoryDisclosureIndicator
            else:
                cell.accessoryType = UITableViewCellAccessoryNone
        else:
            if cell.textLabel.text == table.interface.checkmark:
                cell.accessoryType = UITableViewCellAccessoryCheckmark
            else:
                cell.accessoryType = UITableViewCellAccessoryNone
        return cell

    @objc_method
    def tableView_shouldHighlightRowAtIndexPath_(self, table, index_path):
        if 'widget' in table.interface.data[index_path.row].keys():
            if table.interface.data[index_path.row]['widget'] == 'switch':
                return None
        return index_path

    @objc_method
    def tableView_didSelectRowAtIndexPath_(self, table, index_path):
        if table.interface.checkmark is not None:
            for i in range(len(table.interface.data)):
                index = ObjCClass('NSIndexPath').indexPathForRow_inSection_(i, 0)
                table.cellForRowAtIndexPath_(index).accessoryType = UITableViewCellAccessoryNone
            table.cellForRowAtIndexPath_(index_path).accessoryType = UITableViewCellAccessoryCheckmark
        table.interface.data[index_path.row]['action']()

# _______
# | \ / |
# |[]_[]|  Pfeeeeeeeeeeeert!  Foozy woozy wart!  Thub thub thub thub, poof!  Gorkenshnoggen.  Bleh!
# |_[±]_|  Veewee, Veewee, Veewee!


class WidgetList(Widget):
    def create(self):
        self.native = TogaWidgetList.alloc().init()
        self.native.tableFooterView = UIView.alloc().initWithFrame_(CGRectMake(0, 0, 0, 0))
        self.native.scrollEnabled = False
        self.native.interface = self.interface
        self.native._impl = self
        self.native.columnAutoresizingStyle = 1
        self.native.delegate = self.native
        self.native.dataSource = self.native
        self.add_constraints()

    def reload_data(self):
        self.native.reloadData()

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
