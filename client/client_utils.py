from os import getenv
from os.path import exists
from json import dump, loads

from textual.widgets import ListView

import sounddevice as sd


class ContactsManager:
    def __init__(self):
        super(ContactsManager, self).__init__()

        self.contacts_data = {}
        self._contacts_widget = None
        self.contacts_list = None

        self.path = f"{getenv("HOME")}/tars/comm/contacts.json"
        if exists(self.path):
            self.read_contacts()
        else:
            with open(self.path, "w") as contacts_file:
                dump({}, contacts_file)
                contacts_file.close()

    def set_contacts_list_widget(self, widget):
        self._contacts_widget = widget


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

        contacts_list: ListView = self._contacts_widget.contacts_view
        contacts_list.append(self._contacts_widget.get_contact_item(name))

    def delete_contact(self, name: str):
        self.contacts_data.pop(name)
    
    def edit_contact(self, name: str, new_name: str, new_number: str):
        self.delete_contact(name)
        self.add_contact(new_name, new_number)

class AudioUtils:
    def __init__(self):
        super(AudioUtils, self).__init__()

        self.input_device = None
        self.output_device = None

    """
    get default audio input and output devices
    args: none
    output: tuple
    """
    def get_default_audio_io_devices(self):
        di = sd.default.device[0]
        di_info = sd.query_devices(di, "input")
        do_info = sd.query_devices(di, "output")

        self.input_device = di_info['name']
        self.output_device = do_info['name']

        return (self.input_device, self.output_device)
    
