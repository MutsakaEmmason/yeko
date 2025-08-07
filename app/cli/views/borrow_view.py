from textual.screen import Screen
from textual.widgets import Header, Footer, Input, Button, DataTable, Static
from textual.containers import VerticalScroll, Horizontal
from app.utils.db import SessionLocal
from app.models.models import BorrowedRecord


class BorrowView(Screen):

    def compose(self):
        yield Header()
        yield Static("📄 Borrowed Records", classes="title")

        yield VerticalScroll(
            DataTable(id="borrow_table"),
            Static("Add Borrow Record"),
            Input(placeholder="User ID", id="user_id"),
            Input(placeholder="Book ID", id="book_id"),
            Input(placeholder="Borrow Date (YYYY-MM-DD)", id="borrow_date"),
            Input(placeholder="Due Date (YYYY-MM-DD)", id="due_date"),
            Horizontal(
                Button("➕ Add Record", id="add_record"),
                Button("🔙 Back", id="back"),
            )
        )
        yield Footer()

    def on_mount(self):
        self.query_one("#borrow_table", DataTable).add_columns("ID", "User", "Book", "Borrowed", "Due")
        self.load_records()

    def load_records(self):
        table = self.query_one("#borrow_table", DataTable)
        table.clear()
        with SessionLocal() as db:
            records = db.query(BorrowedRecord).all()
            for r in records:
                table.add_row(str(r.id), str(r.user_id), str(r.book_id), str(r.borrow_date), str(r.due_date))

    def on_button_pressed(self, event):
        if event.button.id == "add_record":
            user_id = self.query_one("#user_id", Input).value
            book_id = self.query_one("#book_id", Input).value
            borrow_date = self.query_one("#borrow_date", Input).value
            due_date = self.query_one("#due_date", Input).value

            with SessionLocal() as db:
                record = BorrowedRecord(user_id=user_id, book_id=book_id, borrow_date=borrow_date, due_date=due_date)
                db.add(record)
                db.commit()

            self.load_records()

        elif event.button.id == "back":
            self.app.pop_screen()
