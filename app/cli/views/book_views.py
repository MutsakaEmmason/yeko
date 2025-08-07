from textual.screen import Screen
from textual.widgets import Header, Footer, Static, DataTable, Button
from textual.containers import VerticalScroll
from app.services.book_service import get_all_books
from textual.widgets import Input
from app.services.book_service import add_book


class BookView(Screen):
    def compose(self):
        yield Header()
        yield Static("📘 Book Inventory", classes="title")
        self.data_table = DataTable(zebra_stripes=True)
        yield VerticalScroll(self.data_table)
        yield Button("⬅ Back to Menu", id="back")
        yield Footer()
        
        yield Static("➕ Add Book")
        yield Horizontal(
            Input(placeholder="Title", id="title"),
            Input(placeholder="Author", id="author"),
            Input(placeholder="Category ID", id="category"),
            Input(placeholder="Total Copies", id="total"),
            Input(placeholder="Available Copies", id="available"),
        )
        yield Button("Add Book", id="add_book")

    def on_mount(self):
        self.load_books()

    def load_books(self):
        self.data_table.clear()
        self.data_table.cursor_type = "row"
        self.data_table.add_columns("ID", "Title", "Author", "Category", "Available", "Total")
        books = get_all_books()
        for book in books:
            self.data_table.add_row(
                str(book["ID"]),
                book["Title"],
                book["Author"],
                book["Category"],
                str(book["Available"]),
                str(book["Total"])
            )

    def on_button_pressed(self, event):
        if event.button.id == "back":
            self.app.pop_screen()
            
        if event.button.id == "add_book":
            title = self.query_one("#title", Input).value
            author = self.query_one("#author", Input).value
            category_id = int(self.query_one("#category", Input).value)
            total = int(self.query_one("#total", Input).value)
            available = int(self.query_one("#available", Input).value)
            add_book(title, author, category_id, total, available)
            self.load_books()

