from time import sleep
from os import getenv
from os.path import exists
from json import dump, loads
from threading import Lock

from textual.app import App
from textual.widgets import ListView, ProgressBar

import sounddevice as sd
from numpy import linalg


class ContactsManager:
    def __init__(self):
        super(ContactsManager, self).__init__()

        self.contacts_data = {}
        self._contacts_widget = None
        self.contacts_list = None
        self.file = None

        self.path = f"{getenv("HOME")}/tars/comm/contacts.json"
        if exists(self.path):
            self.file = open(self.path, "w")
        else:
            with open(self.path, "w") as contacts_file:
                dump({}, contacts_file)
                contacts_file.close()

            self.file = open(self.path, "w")

    def set_contacts_list_widget(self, widget):
        self._contacts_widget = widget

    def get_contacts(self):
        return self.contacts_data.keys()

    def add_contact(self, name: str, number: str):
        self.contacts_data[name] = {
            "name": name,
            "number": number,
        }

        contacts_list: ListView = self._contacts_widget.contacts_view
        contacts_list.append(self._contacts_widget.get_contact_item(name))

        dump(self.contacts_data, self.file)

    def delete_contact(self, name: str):
        self.contacts_data.pop(name)
        dump(self.contacts_data, self.file)

    def edit_contact(self, name: str, new_name: str, new_number: str):
        self.delete_contact(name)
        self.add_contact(new_name, new_number)

class AudioUtils:
    def __init__(self):
        super(AudioUtils, self).__init__()

        self.input_device = None
        self.output_device = None

        self.volume = 0

        self.stream = sd.InputStream(samplerate=44100, blocksize=1024, callback=self.input_audio_callback)

    def start_stream(self):
        self.stream.start()

    """
    get default audio input and output devices
    args: none
    output: tuple
    """
    def get_default_audio_io_devices(self):
        di = sd.default.device[0]
        do = sd.default.device[1]
        di_info = sd.query_devices(di, "input")
        do_info = sd.query_devices(do, "output")

        self.input_device = di_info['name']
        self.output_device = do_info['name']

        return (self.input_device, self.output_device)

    def input_audio_callback(self, indata, frames, time, status):
        self.volume = linalg.norm(indata)*10
