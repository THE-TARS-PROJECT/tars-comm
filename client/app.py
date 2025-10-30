from textual import on
from textual.screen import Screen
from textual.app import App, ComposeResult
from textual.containers import VerticalGroup, HorizontalGroup
from textual.widgets import Static, Header, Footer, Input, Button, Label

from client_auth import Authenticator

auth = Authenticator()

"""
Custom Footer

Will show application state and messages across the app, the built-in footer is kind of restricting
"""
class AppFooter(Static):

    def compose(self) -> ComposeResult:
        stat_label = Label("STATUS: ")
        stat_val = Label("IDLE", id="sys-stat")

        h_container = HorizontalGroup(stat_label, stat_val)
        yield h_container

    def update_status(self, status: str):
        stat_val = self.get_widget_by_id("sys-stat")
        stat_val.update(status)

class LoginScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        header = Header(show_clock=True)

        self.email = Input(placeholder="Email", type="text", validate_on=['submitted'], classes='input-box')
        self.password = Input(placeholder="Password", type="text", validate_on=['submitted'], classes='input-box')

        submit_btn = Button("AUTHENTICATE", id="auth_btn")
        submit_btn.flat = True
        

        fields_container = VerticalGroup(
            self.email, 
            self.password, 
            submit_btn, 
            classes="centered-container"
        )

        self.footer = AppFooter()

        yield header
        yield fields_container
        yield self.footer

    @on(Button.Pressed, "#auth_btn")
    async def login_btn(self, event: Button.Pressed):
        res = auth.login_user(
            email=self.email.value,
            password=self.password.value
        )
        if res != None:
            auth.edit_config("name", res[0])
            auth.edit_config("ph_no", res[1])
            self.footer.update_status("[green]ACCESS GRANTED....[/green]")

        else:
            self.footer.update_status("[red]ACCESS DENIED....[/red]")


class App_(App):
    SCREENS = {"login": LoginScreen}
    CSS_PATH = "style.tcss"

    def on_mount(self):
        self.screen.title = "TARS COMMUNICATION PROTOCOL"

        data = auth.config
        if data["ph_no"] == "":
            self.push_screen("login")
            self.screen.title = "PROTOCOL AUTHENTICATION"

if __name__ == "__main__":
    App_().run()
