from textual.screen import Screen
from textual.widgets import Header, Footer, Input, Button, DataTable, Static
from textual.containers import VerticalScroll, Horizontal
from app.utils.db import SessionLocal
from app.models.models import User, Role


class UserView(Screen):

    def compose(self):
        yield Header()
        yield Static("👤 Manage Users", classes="title")

        yield VerticalScroll(
            DataTable(id="user_table"),
            Static("Add New User"),
            Input(placeholder="Username", id="username"),
            Input(placeholder="Password", id="password", password=True),
            Input(placeholder="Role ID (e.g., 1)", id="role_id"),
            Horizontal(
                Button("➕ Add User", id="add_user"),
                Button("🔙 Back", id="back"),
            )
        )
        yield Footer()

    def on_mount(self):
        self.query_one("#user_table", DataTable).add_columns("ID", "Username", "Role")
        self.load_users()

    def load_users(self):
        table = self.query_one("#user_table", DataTable)
        table.clear()
        with SessionLocal() as db:
            users = db.query(User).all()
            for user in users:
                table.add_row(str(user.id), user.username, str(user.role_id))

    def on_button_pressed(self, event):
        if event.button.id == "add_user":
            username = self.query_one("#username", Input).value
            password = self.query_one("#password", Input).value
            role_id = self.query_one("#role_id", Input).value

            with SessionLocal() as db:
                new_user = User(username=username, password=password, role_id=role_id)
                db.add(new_user)
                db.commit()

            self.load_users()

        elif event.button.id == "back":
            self.app.pop_screen()
