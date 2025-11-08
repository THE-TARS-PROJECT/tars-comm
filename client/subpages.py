from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.css.query import NoMatches
from textual.containers import VerticalGroup, Grid, Horizontal, Vertical
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

class AddContactDialog(Screen):
    
    def compose(self) -> ComposeResult:
        self.header = SubpageHeader()
        self.header.set_title("ADD CONTACT")
        self.header.styles.margin = (0, 4, 0, 0)

        c_name_input = Input(placeholder="Contact Name", max_length=20)
        c_num_input = Input(placeholder="Contact Number", max_length=10, type="number")

        add_btn = Button("Add", id="add-contact")
        discard_btn = Button("Discard", id="discard-btn")

        add_btn.styles.width = "1fr"
        discard_btn.styles.width = "1fr"

        btn_box = Horizontal(
            add_btn, discard_btn
        )

        main_content = Vertical(
            Horizontal(
                Label("Name: "), c_name_input
            ),
            Horizontal(
                Label("Number: "), c_num_input
            ),
            btn_box
        )

        main_content.styles.border = ('heavy', 'yellow')
        main_content.border_title = "Add Contact"

        main_content.styles.width = "50%"
        main_content.styles.height = "20"

        parent = Vertical(main_content)
        parent.styles.align_vertical = "middle"
        parent.styles.align_horizontal = "center"

        yield parent

    
    @on(Button.Pressed, "#add_contact_btn")
    def on_button_pressed(self, event):
        name = self.nameInput.value
        number = self.numberInput.value

        if name != "" and number != "":
            contacts_manager.add_contact(name, number)

"""
ContactList

simple contact list. that's it
"""
class ContactList(Static):
    BINDINGS = [
        ('a', "add_contact", "Add New Contact"),
        ('d', "delete_contact", "Delete contact")
    ]
    def __init__(self):
        super(ContactList, self).__init__()

        self.contacts_view = ListView(id="contacts-list")
    
    def compose(self) -> ComposeResult:
        t_header = SubpageHeader()
        t_header.set_title("CONTACT LISTS")

        contacts_manager.set_contacts_list_widget(self)
        self.contacts = contacts_manager.get_contacts()

        w_layout = VerticalGroup(t_header, self.contacts_view)
        yield w_layout

    def on_mount(self, event):
        for index, contact in enumerate(self.contacts):
            contact_item = ContactItem(contact)
            self.contacts_view.insert(index, [contact_item])

    def gen_tree(self):
        with open('./tree.txt', "w") as tree:
            tree.write(str(self.app.css_tree))

    def get_contact_item(self, name: str):
        return ContactItem(name)

    def action_add_contact(self):
        self.app.push_screen('add_contact')

    def action_delete_contact(self):
        item = self.contacts_view.highlighted_child
        label = item.query_one(Label)
        contacts_manager.delete_contact(label.content)
        self.contacts_view.remove_children([item])

    @on(ListView.Selected)
    def on_item_selected(self, event: ListView.Selected):
        pass


"""
RecentCallPanel

Shows recent calls, numbers (or name if saved) and time of call
"""
class RecentCallPanel(Static):

    def compose(self) -> ComposeResult:
        t_header = SubpageHeader()
        t_header.set_title("RECENT CALLS")

        self.items = []
        contacts_view = ListView()
        for contact in self.items:
            contacts_view._add_child(ContactItem(contact))

        w_layout = VerticalGroup(t_header, contacts_view)

        yield w_layout
