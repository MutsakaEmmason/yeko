from textual.screen import Screen
from textual.widgets import Header, Footer, Input, Button, Static
from textual.containers import Vertical
from app.services.user_service import authenticate_user


class LoginView(Screen):
    def compose(self):
        yield Header()
        yield Static("🔐 Login to Library System", classes="title")
        yield Input(placeholder="Email", id="email")
        yield Input(password=True, placeholder="Password", id="password")
        yield Button("Login", id="login")
        yield Static("", id="error")
        yield Footer()

    def on_button_pressed(self, event):
        if event.button.id == "login":
            email = self.query_one("#email", Input).value
            password = self.query_one("#password", Input).value
            user = authenticate_user(email, password)
            if user:
                self.app.user = user  # store logged-in user
                self.app.push_screen("menu")
            else:
                self.query_one("#error", Static).update("❌ Invalid credentials")
