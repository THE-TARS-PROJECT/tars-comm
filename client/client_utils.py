from os.path import exists
from json import dump, loads
from queue import SimpleQueue
from asyncio import get_running_loop
from os import getenv, path, makedirs

from textual.widgets import ListView

import sounddevice as sd
from numpy import linalg

from dbus_fast.aio import MessageBus

class ContactsManager:
    def __init__(self):
        super(ContactsManager, self).__init__()

        self.contacts_data = {}
        self._contacts_widget = None
        self.contacts_list = None
        self.file = None

        self.path = f"{getenv('HOME')}/tars/comm/contacts.json"
        
        if exists(self.path):
            with open(self.path, "r") as file:
                self.contacts_data = loads(file.read())
                file.close()

        else:
            makedirs(path.dirname(self.path), exist_ok=True)
            with open(self.path, "w") as file:
                dump(self.contacts_data, file)
                file.close()

    def set_contacts_list_widget(self, widget):
        self._contacts_widget = widget

    def get_contacts(self):
        return self.contacts_data.keys()

    def add_contact(self, name: str, number: str):
        if name in self.contacts_data.keys() or number in [num['number'] for num in self.contacts_data.values()]:
            return "already exists"
        self.contacts_data[name] = {
            "name": name,
            "number": number,
        }

        contacts_list: ListView = self._contacts_widget.contacts_view
        contacts_list.append(self._contacts_widget.get_contact_item(name))

        self.dump_data()

    def delete_contact(self, name: str):
        self.contacts_data.pop(name)
        self.dump_data()
    
    def edit_contact(self, name: str, new_name: str, new_number: str):
        self.delete_contact(name)
        self.add_contact(new_name, new_number)

    def dump_data(self):
        with open(self.path, "w") as file:
            dump(self.contacts_data, file)

class AudioUtils:
    def __init__(self):
        super(AudioUtils, self).__init__()

        self.audio_buffer = SimpleQueue()
        self.out_audio_buffer = SimpleQueue()

        self.input_device = None
        self.output_device = None
        self.dbus_interface = None

        self.volume = 0

        self.in_stream = sd.InputStream(samplerate=44100, blocksize=1024, callback=self.input_audio_callback, dtype="float32")
        self.out_stream = sd.OutputStream(samplerate=44100, blocksize=1024, callback=self.on_audio_packet_recvd)

    async def dbus_worker(self):
        while True:
            loop = get_running_loop()
            data_b = await loop.run_in_executor(None, self.audio_buffer.get)
            await self.dbus_interface.call_send_audio_packet(data_b)

    async def audio_recv_dbus_worker(self):
        while True:
            loop = get_running_loop()
            data_b = await loop.run_in_executor(None, self.out_audio_buffer.get)
            self.out_stream.write(data_b)
    
    def start_stream(self):
        self.in_stream.start()

    def start_out_stream(self):
        if self.dbus_interface:
            self.out_stream.start()
            self.dbus_interface.incoming_audio(self.on_audio_packet_recvd)

    def on_audio_packet_recvd(self, packet: bytes):
        self.out_audio_buffer.put_nowait(packet)


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
        if self.dbus_interface is None:
            self.volume = 0
        self.audio_buffer.put_nowait(indata.tobytes())


class ClientDBUS:
    def __init__(self):
        super(ClientDBUS, self).__init__()

        self.bus, self.obj, self.interface = None, None, None

    async def setup(self):
        self.bus = await MessageBus().connect()
        intros = await self.bus.introspect(
            "com.cooper.tars",
            "/cooper/tars/comm"
        )
        self.obj = self.bus.get_proxy_object(
            "com.cooper.tars",
            "/cooper/tars/comm",
            intros
        )
        self.interface = self.obj.get_interface("com.cooper.tars.interface")

    def get_interface(self):
        return self.interface    

