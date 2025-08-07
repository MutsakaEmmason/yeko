from textual.screen import Screen
from textual.widgets import Header, Footer, Static, DataTable, Button
from textual.containers import VerticalScroll
from app.services.user_service import get_all_users
from textual.containers import Horizontal
from textual.widgets import Input
from app.services.user_service import add_user

class UserView(Screen):
    def compose(self):
        yield Header()
        yield Static("👤 User Management", classes="title")
        self.data_table = DataTable(zebra_stripes=True)
        yield VerticalScroll(self.data_table)
        yield Button("⬅ Back to Menu", id="back")
        yield Footer()
        yield Static("➕ Add User")
        yield Horizontal(
            Input(placeholder="Name", id="name"),
            Input(placeholder="Email", id="email"),
            Input(placeholder="Password", id="password", password=True),
            Input(placeholder="Role ID (1=Librarian, 2=Student)", id="role")
        )
        yield Button("Add User", id="add")

    def on_mount(self):
        self.load_users()

    def load_users(self):
        self.data_table.clear()
        self.data_table.cursor_type = "row"
        self.data_table.add_columns("ID", "Name", "Email", "Role")
        users = get_all_users()
        for user in users:
            self.data_table.add_row(
                str(user["ID"]),
                user["Name"],
                user["Email"],
                user["Role"]
            )

    def on_button_pressed(self, event):
        if event.button.id == "back":
            self.app.pop_screen()
        if event.button.id == "add":
            name = self.query_one("#name", Input).value
            email = self.query_one("#email", Input).value
            password = self.query_one("#password", Input).value
            role_id = int(self.query_one("#role", Input).value)
            add_user(name, email, password, role_id)
            self.load_users()

