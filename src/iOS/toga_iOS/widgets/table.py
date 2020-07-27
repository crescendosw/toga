from travertino.size import at_least

from toga.sources import to_accessor
from toga_iOS.libs import *

from .base import Widget
# from .internal.cells import TogaIconCell
# from .internal.data import TogaData

from rubicon.objc import ObjCClass


class TogaTable(UITableView):
    # TableDataSource methods
    @objc_method
    def tableView_numberOfRowsInSection_(self, table) -> int:
        # print('numberOfRows called')
        print(table.interface.headings)
        return 5#len(self.interface.data) if self.interface.data else 0

    @objc_method
    def numberOfSectionsInTableView_(self) -> int:
        # print('numberOfSections called')
        return 1

    @objc_method
    def tableView_cellForRowAtIndexPath_(self, index_path) -> type(UITableViewCell):
        # print('cellForRow called')
        print(self.interface.headings)  # boom roasted
        print(index_path)
        cell_identifier = 'cell identifier'
        cell = self.dequeueReusableCellWithIdentifier_(cell_identifier)
        if not cell:
            cell = UITableViewCell.alloc().initWithStyle_reuseIdentifier_(UITableViewCellStyleDefault, cell_identifier)
        cell.textLabel.text = 'Text'
        print(cell)
        return cell


#
#     @objc_method
#     def tableView_objectValueForTableColumn_row_(self, table, column, row: int):
#         data_row = self.interface.data[row]
#         try:
#             data = data_row._impls
#         except AttributeError:
#             data = {
#                 attr: TogaData.alloc().init()
#                 for attr in self.interface._accessors
#             }
#             data_row._impls = data
#
#         col_identifier = str(column.identifier)
#
#         datum = data[col_identifier]
#         value = getattr(data_row, col_identifier)
#
#         # Allow for an (icon, value) tuple as the simple case
#         # for encoding an icon in a table cell.
#         if isinstance(value, tuple):
#             icon, value = value
#         else:
#             # If the value has an icon attribute, get the _impl.
#             # Icons are deferred resources, so we bind to the factory.
#             try:
#                 icon = value.icon.bind(self.interface.factory)
#             except AttributeError:
#                 icon = None
#
#         datum.attrs = {
#             'label': str(value),
#             'icon': icon,
#         }
#
#         return datum
#
#     # TableDelegate methods
#     @objc_method
#     def selectionShouldChangeInTableView_(self, table) -> bool:
#         # Explicitly allow selection on the table.
#         # TODO: return False to disable selection.
#         return True
#
#     @objc_method
#     def tableViewSelectionDidChange_(self, notification) -> None:
#         selection = []
#         current_index = self.selectedRowIndexes.firstIndex
#         for i in range(self.selectedRowIndexes.count):
#             selection.append(self.interface.data[current_index])
#             current_index = self.selectedRowIndexes.indexGreaterThanIndex(current_index)
#
#         if not self.interface.multiple_select:
#             try:
#                 self.interface._selection = selection[0]
#             except IndexError:
#                 self.interface._selection = None
#         else:
#             self.interface._selection = selection
#
#         if notification.object.selectedRow == -1:
#             selected = None
#         else:
#             selected = self.interface.data[notification.object.selectedRow]
#
#         if self.interface.on_select:
#             self.interface.on_select(self.interface, row=selected)
#

class Table(Widget):
    def create(self):
        # Create a table view, and put it in a scroll view.
        # The scroll view is the native, because it's the outer container.
        #self.native = UIScrollView.alloc().init()
        # self.native.hasVerticalScroller = True
        # self.native.hasHorizontalScroller = False
        # self.native.autohidesScrollers = False
        # self.native.borderType = 2

        self.native = TogaTable.alloc().init()#WithFrame_style_(((0, 0), (500, 500)), 0)
        print(dir(self.native.bounds))
        self.native.bounds.size.width = -500.0
        self.native.bounds.size.height = 500.0
        self.native.bounds = ((0.0, 0.0), (500.0, 500.0))
        print(self.native.bounds.origin.x)
        print(self.native.bounds.origin.y)
        print(self.native.bounds.size.width)
        print(self.native.bounds.size.height)
        print(self.native.frame)
        self.native.interface = self.interface
        self.native._impl = self
        self.native.columnAutoresizingStyle = 1

        # self.table.allowsMultipleSelection = self.interface.multiple_select

        # Create columns for the table
        # self.columns = []
        # Cocoa identifies columns by an accessor; to avoid repeated
        # conversion from ObjC string to Python String, create the
        # ObjC string once and cache it.
        # self.column_identifiers = {}
        # for i, (heading, accessor) in enumerate(zip(
        #             self.interface.headings,
        #             self.interface._accessors
        #         )):
        #
        #     column_identifier = at(accessor)
        #     self.column_identifiers[id(column_identifier)] = accessor
        #     column = NSTableColumn.alloc().initWithIdentifier(column_identifier)
        #     self.table.addTableColumn(column)
        #     self.columns.append(column)
        #
        #     cell = TogaIconCell.alloc().init()
        #     column.dataCell = cell
        #
        #     column.headerCell.stringValue = heading

        self.native.delegate = self.native
        self.native.dataSource = self.native

        # Embed the table view in the scroll view
        #self.native.documentView = self.table

        #self.native.

        # Add the layout constraints
        self.add_constraints()

    def change_source(self, source):
        self.native.reloadData()

    def insert(self, index, item):
        self.native.reloadData()

    def change(self, item):
        self.native.reloadData()

    def remove(self, item):
        self.native.reloadData()

    def clear(self):
        self.native.reloadData()

    def set_on_select(self, handler):
        pass

    def scroll_to_row(self, row):
        self.native.scrollRowToVisible(row)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
