from textual import on
from textual.screen import Screen
from textual.css.query import NoMatches
from textual.app import App, ComposeResult
from textual.widgets import Static, Header, Input, Button, Label
from textual.containers import VerticalGroup, HorizontalGroup, Vertical, Horizontal

from client_utils import AudioUtils
from client_auth import Authenticator


from subpages import ContactList, RecentCallPanel, AddContactDialog

auth = Authenticator()
audio_helper = AudioUtils()

"""
Custom Footer

Will show application state and messages across the app, the built-in footer is kind of restricting
"""
class AppFooter(Static):
    def __init__(self):
        super(AppFooter, self).__init__()

        self.status = ""

    def compose(self) -> ComposeResult:
        stat_label = Label("STATUS: ")
        stat_val = Label("IDLE", id="sys-stat")

        h_container = HorizontalGroup(stat_label, stat_val)
        yield h_container

    def on_mount(self, event):
        self.update_status(self.status)

    def update_status(self, status: str):
        try:
            stat_val = self.get_widget_by_id("sys-stat")
            stat_val.update(status)

        except NoMatches:
            self.status = status

"""
Login Screen

shows when json field is empty
"""
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

"""
HomeScreen

shows contact list, recent calls, and ongoing call status
"""
class HomeScreen(Screen):
    
    def compose(self):
        contacts_list_widget = ContactList()
        recent_calls_widget = RecentCallPanel()

        active_microphone, active_od = audio_helper.get_default_audio_io_devices()
        am_label = Label(f"Input Device: {active_microphone}")
        od_label = Label(f"Output Device: {active_od}")

        contacts_list_widget.styles.height = "50%"
        contacts_list_widget.styles.min_width = "30%"
        contacts_list_widget.styles.max_width = "50%"

        recent_calls_widget.styles.height = "50%"
        recent_calls_widget.styles.min_width = "30%"
        recent_calls_widget.styles.max_width = "50%"

        home_layout = Vertical(contacts_list_widget, recent_calls_widget)
        main_content = Horizontal(
            Vertical(
                am_label, od_label, id="main-content_", classes="main_content_"
            )
        )

        self.app_footer = AppFooter()
        self.app_footer.update_status("[green]CONNECTED[/green]")

        yield Header(show_clock=True)
        yield Horizontal(home_layout, main_content)
        yield self.app_footer

"""
main app
dont touch
"""
class App_(App):
    SCREENS = {
        "login": LoginScreen,
        "home": HomeScreen,
        "add_contact": AddContactDialog
    }
    CSS_PATH = "style.tcss"

    def on_mount(self):
        self.screen.title = "TARS COMMUNICATION PROTOCOL"

        data = auth.config
        if data["ph_no"] == "":
            self.push_screen("login")
            self.screen.title = "PROTOCOL AUTHENTICATION"

        else:
            self.push_screen("home")
            self.screen.title = "TARS COMMUNICATION PROTOCOL"

if __name__ == "__main__":
    App_().run()
