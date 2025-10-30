from os import getenv
from os.path import exists
from json import dump, loads

class ContactsManager:
    def __init__(self):
        super(ContactsManager, self).__init__()

        self.contacts_data = {}

        self.path = f"{getenv("HOME")}/tars/comm/contacts.js"
        if exists(self.path):
            self.read_contacts()
        else:
            with open(self.path, "w") as contacts_file:
                dump({}, contacts_file)
                contacts_file.close()

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

    def delete_contact(self, name: str):
        self.contacts_data.pop(name)
    
    def edit_contact(self, name: str, new_name: str, new_number: str):
        self.delete_contact(name)
        self.add_contact(new_name, new_number)