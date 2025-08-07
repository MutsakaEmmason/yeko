from textual.screen import Screen
from textual.widgets import Header, Footer, Static, DataTable, Button
from textual.containers import VerticalScroll
from app.services.report_service import get_all_reports


class ReportView(Screen):
    def compose(self):
        yield Header()
        yield Static("📊 Reports", classes="title")
        self.data_table = DataTable(zebra_stripes=True)
        yield VerticalScroll(self.data_table)
        yield Button("⬅ Back to Menu", id="back")
        yield Footer()

    def on_mount(self):
        self.load_reports()

    def load_reports(self):
        self.data_table.clear()
        self.data_table.cursor_type = "row"
        self.data_table.add_columns("ID", "Type", "By", "Date", "Description")
        reports = get_all_reports()
        for r in reports:
            self.data_table.add_row(
                str(r["ID"]),
                r["Type"],
                r["By"],
                str(r["Date"]),
                r["Description"]
            )

    def on_button_pressed(self, event):
        if event.button.id == "back":
            self.app.pop_screen()
