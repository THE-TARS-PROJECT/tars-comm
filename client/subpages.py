from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.css.query import NoMatches
from textual.containers import VerticalGroup, HorizontalGroup
from textual.widgets import Static, Label, ListView, ListItem, Input, Button

from client_utils import ContactsManager

contacts_manager = ContactsManager()


class ContactItem(ListItem):
    def __init__(self, contact_name: str):
        super(ContactItem, self).__init__()

        self.contact_name = contact_name
        self.id = f"{self.contact_name}".lower().replace(" ", "")
        
    def compose(self) -> ComposeResult:
        yield Label(self.contact_name)


class SubpageHeader(Static):
    def __init__(self):
        super(SubpageHeader, self).__init__()

        self.pending_title = ""
        self.classes = "custom_header"

    def compose(self):
        yield Label("", id="title")
        return super().compose()
    
    async def on_mount(self, _):
        self.set_title(self.pending_title)
        self.pending_title = ""
    
    def set_title(self, title: str):
        try:
            title_label = self.get_widget_by_id("title")
            title_label.update(title)

        except NoMatches:
            self.pending_title = title

class AddContactDialog(ModalScreen):
    classes="add-contact-dialog"
    BINDINGS = [
        ("c", "discard", "Discard Contact")
    ]
    
    def compose(self) -> ComposeResult:
        self.header = SubpageHeader()
        self.header.set_title("Add Contact")

        self.nameInput = Input(placeholder="Name", type="text", validate_on=['submitted'], classes='input-box')
        self.numberInput = Input(placeholder="Phone Number", type="integer", validate_on=['submitted'], classes='input-box', max_length=10)
        add_btn  = Button("Add", flat=True, id="add_contact_btn")
        discard_btn = Button("Discard", flat=True, id="discard_btn")

        btn_layout = HorizontalGroup(add_btn, discard_btn)
        layout = VerticalGroup(self.nameInput, self.numberInput, btn_layout)

        yield layout

    @on(Button.Pressed, "#add_contact_btn")
    def on_button_pressed(self, event):
        name = self.nameInput.value
        number = self.numberInput.value

        if name != "" and number != "":
            contacts_manager.add_contact(name, number)

    @on(Button.Pressed, "#discard_btn")
    def close_dialog(self, event):
        self.dismiss(True)

"""
ContactList

simple contact list. that's it
"""
class ContactList(Static):
    BINDINGS = [
        ('a', "add_contact", "Add New Contact")
    ]
    def __init__(self):
        super(ContactList, self).__init__()

        self.contacts_view = ListView(id="contacts-list")
    
    def compose(self) -> ComposeResult:
        t_header = SubpageHeader()
        t_header.set_title("CONTACT LISTS")

        contacts_manager.set_contacts_list_widget(self)
        self.contacts = contacts_manager.get_contacts()

        for contact in self.contacts:
            contact_item = ContactItem(contact)
            self.contacts_view._add_child(contact_item)


        w_layout = VerticalGroup(t_header, self.contacts_view)

        yield w_layout

    def get_contact_item(self, name: str):
        return ContactItem(name)

    def action_add_contact(self):
        self.app.push_screen('add_contact')

    @on(ListView.Selected)
    def on_item_selected(self, event: ListView.Selected):
        self.app.push_screen('add_contact')


"""
RecentCallPanel

Shows recent calls, numbers (or name if saved) and time of call
"""
class RecentCallPanel(Static):

    def compose(self) -> ComposeResult:
        t_header = SubpageHeader()
        t_header.set_title("RECENT CALLS")

        self.items = [
            "Raghav",
            "Tanmay",
            "Aashish",
            "Jitu Sir"
        ]
        contacts_view = ListView()
        for contact in self.items:
            contacts_view._add_child(ContactItem(contact))

        w_layout = VerticalGroup(t_header, contacts_view)

        yield w_layout
