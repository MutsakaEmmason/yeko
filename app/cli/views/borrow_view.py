from textual.screen import Screen
from textual.widgets import Header, Footer, Static, DataTable, Button
from textual.containers import VerticalScroll
from app.services.borrow_service import get_all_borrowed_records


class BorrowView(Screen):
    def compose(self):
        yield Header()
        yield Static("📄 Borrowed Books", classes="title")
        self.data_table = DataTable(zebra_stripes=True)
        yield VerticalScroll(self.data_table)
        yield Button("⬅ Back to Menu", id="back")
        yield Footer()

    def on_mount(self):
        self.load_records()

    def load_records(self):
        self.data_table.clear()
        self.data_table.cursor_type = "row"
        self.data_table.add_columns("ID", "User", "Book", "Borrow Date", "Due Date", "Return Date", "Status")
        records = get_all_borrowed_records()
        for r in records:
            self.data_table.add_row(
                str(r["ID"]),
                r["User"],
                r["Book"],
                str(r["Borrow Date"]),
                str(r["Due Date"]),
                str(r["Return Date"]),
                r["Status"]
            )

    def on_button_pressed(self, event):
        if event.button.id == "back":
            self.app.pop_screen()
