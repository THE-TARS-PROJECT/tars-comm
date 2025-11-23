from textual import on
from textual.screen import Screen
from textual.app import ComposeResult
from widgets import ContactList, RecentCallPanel
from textual.containers import Vertical, Horizontal, VerticalGroup
from textual.widgets import Header, Input, Label, ProgressBar, Button

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
            self.auth.edit_config("refresh_token", res[3])
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
HomeScreen

shows contact list, recent calls, and ongoing call status
"""
class HomeScreen(Screen):
    def __init__(self):
        super(HomeScreen, self).__init__()

        self.dbus_interface = self.app.shared_instances['dbus_interface']
        self.dbus_interface.on_on_call_response(self.handle_call_response)

        self.audio_helper = self.app.shared_instances['audio_helper']
    prog_bar = None

    BINDINGS = [
        ('c', "show_dial_screen", "Dial Contact")
    ]

    async def on_mount(self):
        self.set_interval(0.05, self.update_prog)

    def handle_call_response(self, data):
        self.app_footer.update_status("INCOMING CALL....")

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

    async def update_prog(self):
        if self.prog_bar != None:
            self.prog_bar.update(progress=int(self.audio_helper.volume))

    def compose(self):
        contacts_list_widget = ContactList()
        recent_calls_widget = RecentCallPanel()

        contacts_list_widget.styles.height = "50%"
        recent_calls_widget.styles.height = "50%"

        mic_vis = ProgressBar(id="mic_vis", total=100, show_eta=False, show_percentage=False)
        self.prog_bar = mic_vis
        self.audio_helper.start_stream()

        active_microphone, active_od = self.audio_helper.get_default_audio_io_devices()
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
        

class AddContactDialog(Screen):
    def __init__(self):
        super(AddContactDialog, self).__init__()

        self.contacts_manager = self.app.shared_instances['contacts_manager']
    
    def on_mount(self):
        self.set_interval(5.0, self.reset_title)

    def reset_title(self):
        self.border_title = "Add Contact"
    
    def compose(self) -> ComposeResult:

        self.c_name_input = Input(placeholder="Contact Name", max_length=20)
        self.c_num_input = Input(placeholder="Contact Number", max_length=10, type="number")

        add_btn = Button("Add", classes="add-contact", id="add-contact")
        discard_btn = Button("Discard", id="discard-btn")

        add_btn.styles.width = "1fr"
        discard_btn.styles.width = "1fr"

        btn_box = Horizontal(
            add_btn, discard_btn
        )
        btn_box.styles.column_gap = 2
        
        name_row = Horizontal(
            Label("Name: "), self.c_name_input
        )
        
        name_row.styles.column_gap = 2 
        
        name_row.styles.margin_bottom = 1 

        number_row = Horizontal(
            Label("Number: "), self.c_num_input
        )
        
        number_row.styles.column_gap = 2 
        
        number_row.styles.margin_bottom = 2 
        
        self.c_name_input.styles.width = "100%"
        self.c_num_input.styles.width = "100%"

        main_content = Vertical(
            name_row,
            number_row,
            btn_box
        )

        main_content.styles.border = ('heavy', 'blue')
        main_content.border_title = "Add Contact"
        
        main_content.styles.padding = 1
        main_content.styles.width = "50%"
        main_content.styles.height = "50%" 

        parent = Vertical(main_content)
        parent.styles.align_vertical = "middle"
        parent.styles.align_horizontal = "center"

        yield parent
    
    @on(Button.Pressed, "#add-contact")
    def handle_add_contact(self, event):
        self.app.log("clicked add contact button")
        name = self.c_name_input.value
        number = self.c_num_input.value

        if name != "" and number != "":
            x = self.contacts_manager.add_contact(name, number)
            if x == "already exists":
                self.border_title = "Already Exists"
            
            else:
                self.dismiss(True)

        self.dismiss(True)


    @on(Button.Pressed, "#discard-btn")
    def handle_discard(self, event):
        self.dismiss(True)

"""
DailerScreen
Enter a number or select a contact to dial
"""
class DialerScreen(Screen):
    def compose(self) -> ComposeResult:
        self.dbus = self.app.shared_instances['dbus_interface']
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
    async def on_submitted(self, event: Input.Submitted):
        if self.dialer_input.value != "":
            await self.dbus.call_dial_number(self.dialer_input.value)
        self.dismiss(True)
