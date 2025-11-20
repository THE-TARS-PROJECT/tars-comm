from textual import on
from textual.screen import Screen
from textual.css.query import NoMatches
from textual.app import App, ComposeResult
from textual.widgets import Static, Header, Input, Button, Label, ProgressBar
from textual.containers import VerticalGroup, HorizontalGroup, Vertical, Horizontal

from client_auth import Authenticator
from client_socket import ClientService
from client_utils import AudioUtils, ContactsManager


from subpages import ContactList, RecentCallPanel, AddContactDialog

auth = Authenticator()
audio_helper = AudioUtils()

contacts_manager = ContactsManager()

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
            self.app.push_screen("home")
            self.app.title = "TARS COMMUNICATION PROTOCOL"

        else:
            self.footer.update_status("[red]ACCESS DENIED....[/red]")

    CSS_PATH = "./style.tcss"


"""
HomeScreen

shows contact list, recent calls, and ongoing call status
"""
class HomeScreen(Screen):
    def __init__(self):
        super(HomeScreen, self).__init__()
    prog_bar = None

    BINDINGS = [
        ('c', "show_dial_screen", "Dial Contact")
    ]

    async def on_mount(self):
        self.set_interval(0.05, self.update_prog)

    def action_show_dial_screen(self):
        self.app.push_screen("dialer")

    def handle_dialer_dismiss(self, data: dict):
        if not data:
            pass
        else:
            dialer_content = Vertical(
                Label("----------------x----------------"),
                Label(f"Name: {data['name']}"),
                Label(f"Number: {data['number']}"),
            )
            self.main_content._add_child(dialer_content)

    def compose(self):
        contacts_list_widget = ContactList()
        recent_calls_widget = RecentCallPanel()

        contacts_list_widget.styles.height = "50%"
        recent_calls_widget.styles.height = "50%"

        mic_vis = ProgressBar(id="mic_vis", total=100, show_eta=False, show_percentage=False)
        self.prog_bar = mic_vis
        audio_helper.start_stream()

        active_microphone, active_od = audio_helper.get_default_audio_io_devices()
        am_label = Label(f"Input Device: {active_microphone}")
        od_label = Label(f"Output Device: {active_od}")

        left_bar = Vertical(contacts_list_widget, recent_calls_widget)
        left_bar.styles.width = "25%"

        self.main_content = Vertical(am_label, od_label, self.prog_bar, classes="main-content")
        self.main_content.styles.margin = (2,2,2,2)

        main_layout = Horizontal(left_bar, self.main_content)

        self.app_footer = AppFooter()
        self.app_footer.update_status("[green]CONNECTED....[/green]")

        yield Header(show_clock=True)
        yield main_layout
        yield self.app_footer

    async def update_prog(self):
        if self.prog_bar != None:
            self.prog_bar.update(progress=int(audio_helper.volume))

"""
DailerScreen
Enter a number or select a contact to dial
"""
class DialerScreen(Screen):
    def compose(self) -> ComposeResult:
        self.header = Header()

        self.dialer_input = Input(placeholder="Enter number / name of contact: ")
        self.dialer_input.id = "dialer-input"
        main_layout = Vertical(
            self.dialer_input,
        )

        parent = Vertical(main_layout)

        main_layout.styles.width = "50%"
        main_layout.styles.height = "50%"

        parent.styles.align_vertical = "middle"
        parent.styles.align_horizontal = "center"
        parent.styles.border = ('heavy', 'blue')
        parent.border_title = "Dialer"

        yield self.header
        yield parent

    @on(Input.Submitted, "#dialer-input")
    def on_submitted(self, event: Input.Submitted):
        self.dismiss(True)


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
