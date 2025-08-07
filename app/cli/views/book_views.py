from textual.screen import Screen
from textual.widgets import Static, Input, Button, DataTable
from textual.containers import Container, Horizontal
from app.services.book_service import BookService

class BookView(Screen):
    def compose(self):
        yield Static("📚 Book Management", classes="header")

        with Horizontal():
            yield Input(placeholder="Search by title or author...", id="search_input")
            yield Button("Search", id="search_btn")
            yield Button("Sort A-Z", id="sort_btn")

        yield DataTable(id="book_table")

    def on_mount(self):
        self.book_service = BookService()
        self.load_books()

    def load_books(self, search_term="", sort=False):
        books = self.book_service.get_all_books()

        # Filter
        if search_term:
            books = [b for b in books if search_term.lower() in b.title.lower() or search_term.lower() in b.author.lower()]

        # Sort
        if sort:
            books = sorted(books, key=lambda b: b.title.lower())

        table = self.query_one("#book_table", DataTable)
        table.clear()
        table.cursor_type = "row"
        table.add_columns("ID", "Title", "Author", "Year", "Category")

        for book in books:
            table.add_row(str(book.id), book.title, book.author, str(book.year), book.category.name if book.category else "-")

    def on_button_pressed(self, event: Button.Pressed):
        search_term = self.query_one("#search_input", Input).value.strip()

        if event.button.id == "search_btn":
            self.load_books(search_term=search_term)

        elif event.button.id == "sort_btn":
            self.load_books(sort=True)
