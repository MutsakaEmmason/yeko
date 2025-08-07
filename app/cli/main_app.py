from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.containers import Vertical
from textual.screen import Screen
from cli.views.user_view import UserView
from cli.views.book_view import BookView
from cli.views.borrow_view import BorrowView
from cli.views.report_view import ReportView
from cli.views.login_view import LoginView


class MenuScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("📚 Library Management CLI", classes="title")
        yield Vertical(
            Button("📘 Manage Books", id="books"),
            Button("👤 Manage Users", id="users"),
            Button("📄 Borrow Records", id="borrow"),
            Button("📊 Reports", id="reports"),
            Button("🚪 Logout", id="exit"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "books":
                self.app.push_screen(BookView())
            case "users":
                self.app.push_screen(UserView())
            case "borrow":
                self.app.push_screen(BorrowView())
            case "reports":
                self.app.push_screen(ReportView())
            case "exit":
                self.app.pop_screen()
                self.app.pop_screen()


class LibraryApp(App):
    CSS_PATH = "cli/styles.css"

    def on_mount(self) -> None:
        self.user = None
        self.install_screen(LoginView(), name="login")
        self.install_screen(MenuScreen(), name="menu")
        self.push_screen("login")


if __name__ == "__main__":
    app = LibraryApp()
    app.run()
