from travertino.size import at_least

from toga_iOS.libs import *

from .base import Widget


class TogaWidgetList(UITableView):
    @objc_method
    def tableView_numberOfRowsInSection_(self, table) -> int:
        return len(self.interface.headings)

    @objc_method
    def numberOfSectionsInTableView_(self) -> int:
        return 1

    @objc_method
    def tableView_cellForRowAtIndexPath_(self, table, index_path) -> type(UITableViewCell):
        cell_identifier = 'cell identifier'
        cell = self.dequeueReusableCellWithIdentifier_(cell_identifier)
        if not cell:
            cell = UITableViewCell.alloc().initWithStyle_reuseIdentifier_(UITableViewCellStyleDefault, cell_identifier)
        cell.textLabel.text = self.interface.headings[index_path.row]
        self.interface.rows_added += 1
        return cell


class WidgetList(Widget):
    def create(self):
        self.native = TogaWidgetList.alloc().init()
        self.native.interface = self.interface
        self.native._impl = self
        self.native.columnAutoresizingStyle = 1
        self.native.delegate = self.native
        self.native.dataSource = self.native
        self.add_constraints()

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
