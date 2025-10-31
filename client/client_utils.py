from os import getenv
from os.path import exists
from json import dump, loads

from textual._node_list import DuplicateIds

class ContactsManager:
    def __init__(self):
        super(ContactsManager, self).__init__()

        self.contacts_data = {}
        self._contacts_widget = None

        self.path = f"{getenv("HOME")}/tars/comm/contacts.json"
        if exists(self.path):
            self.read_contacts()
        else:
            with open(self.path, "w") as contacts_file:
                dump({}, contacts_file)
                contacts_file.close()

    def set_contacts_list_widget(self, widget):
        self._contacts_widget = widget

    def refresh_contacts_list(self):
        contacts_list = self._contacts_widget.contacts_view
        contacts_list.clear()
        for contact in self.contacts_data.keys():
            item = self._contacts_widget.get_contact_item(contact)
            
            try:
                contacts_list._add_child(item)
                contacts_list.refresh(layout=True)

            except DuplicateIds:
                pass

    def read_contacts(self):
        with open(self.path, "r") as contacts_file:
            self.contacts_data = loads(contacts_file.read())
            contacts_file.close()

    def get_contacts(self):
        return self.contacts_data.keys()

    def add_contact(self, name: str, number: str):
        self.contacts_data[name] = {
            "name": name,
            "number": number,
        }
        with open(self.path, "w") as contacts_file:
            dump(self.contacts_data, contacts_file)
            contacts_file.close()

        self.refresh_contacts_list()

    def delete_contact(self, name: str):
        self.contacts_data.pop(name)
    
    def edit_contact(self, name: str, new_name: str, new_number: str):
        self.delete_contact(name)
        self.add_contact(new_name, new_number)

