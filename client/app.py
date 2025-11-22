from textual import on
from textual.screen import Screen
from textual.app import App, ComposeResult
from textual.containers import VerticalGroup
from textual.widgets import Header, Input, Button

from client_auth import Authenticator
from client_utils import AudioUtils, ContactsManager, ClientDBUS

from screens import DialerScreen, HomeScreen, AddContactDialog

from widgets import AppFooter


"""
Login Screen

shows when json field is empty
"""
class LoginScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def on_mount(self):
        self.auth = self.app.shared_instances['auth']


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
        res = self.auth.login_user(
            email=self.email.value,
            password=self.password.value
        )
        if res != None:
            self.auth.edit_config("name", res[0])
            self.auth.edit_config("ph_no", res[1])
            self.auth.edit_config("access_token", res[2])
            self.footer.update_status("[green]ACCESS GRANTED....[/green]")
            self.app.push_screen("home")
            self.app.title = "TARS COMMUNICATION PROTOCOL"

        else:
            self.footer.update_status("[red]ACCESS DENIED....[/red]")

    CSS_PATH = "./style.tcss"


    async def update_prog(self):
        if self.prog_bar != None:
            self.prog_bar.update(progress=int(self.audio_helper.volume))



"""
main app
dont touch
"""
class App_(App):
    SCREENS = {
        "login": LoginScreen,
        "home": HomeScreen,
        "add_contact": AddContactDialog,
        'dialer': DialerScreen
    }

    CSS_PATH = "style.tcss"

    async def on_mount(self):
        self.auth = Authenticator()
        self.audio_helper = AudioUtils()
        self.contacts_manager = ContactsManager()
        self.dbus = ClientDBUS()

        await self.dbus.setup()

        self.shared_instances = {
            "audio_helper": self.audio_helper,
            "contacts_manager": self.contacts_manager,
            "auth": self.auth,
            "dbus_interface": self.dbus.get_interface()
        }
        self.screen.title = "TARS COMMUNICATION PROTOCOL"

        data = self.auth.config
        if data["ph_no"] == "":
            self.push_screen("login")
            self.screen.title = "PROTOCOL AUTHENTICATION"

        else:
            self.push_screen("home")
            self.screen.title = "TARS COMMUNICATION PROTOCOL"

if __name__ == "__main__":
    App_().run()
