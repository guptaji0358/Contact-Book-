from scripts.main_window import MainWindowMixin
from scripts.table_helpers import TableMixin
from scripts.view_dialog import ViewDialogMixin
from scripts.add_dialog import AddDialogMixin
from scripts.edit_dialog import EditDialogMixin
from scripts.delete_dialog import DeleteDialogMixin
from scripts.import_export import ImportExportMixin
from scripts.call_dialog import CallMixin
from scripts.books_ui import BooksMixin


class ContactBookGUI(
    TableMixin,
    ViewDialogMixin,
    AddDialogMixin,
    EditDialogMixin,
    DeleteDialogMixin,
    ImportExportMixin,
    CallMixin,
    BooksMixin,
    MainWindowMixin,
):
    def __init__(self):
        super().__init__()
        self.BuildMainWindow()
