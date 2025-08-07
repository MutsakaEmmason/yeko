from textual.screen import Screen
from textual.widgets import Header, Footer, Button, DataTable, Static
from textual.containers import VerticalScroll, Horizontal
from app.utils.db import SessionLocal
from app.models.models import Report


class ReportView(Screen):

    def compose(self):
        yield Header()
        yield Static("📊 Reports", classes="title")

        yield VerticalScroll(
            DataTable(id="report_table"),
            Horizontal(
                Button("🔄 Refresh", id="refresh"),
                Button("🔙 Back", id="back"),
            )
        )
        yield Footer()

    def on_mount(self):
        self.query_one("#report_table", DataTable).add_columns("ID", "Title", "Generated At", "Description")
        self.load_reports()

    def load_reports(self):
        table = self.query_one("#report_table", DataTable)
        table.clear()
        with SessionLocal() as db:
            reports = db.query(Report).all()
            for rep in reports:
                table.add_row(str(rep.id), rep.title, str(rep.generated_at), rep.description or "")

    def on_button_pressed(self, event):
        if event.button.id == "refresh":
            self.load_reports()
        elif event.button.id == "back":
            self.app.pop_screen()
