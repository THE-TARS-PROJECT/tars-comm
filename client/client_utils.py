from traceback import print_exc
from os.path import exists
from json import dump, loads
from queue import SimpleQueue, Empty
from asyncio import get_running_loop, sleep
from os import getenv, path, makedirs

from numpy import frombuffer

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

        self.input_buff = SimpleQueue()
        self.output_buff = SimpleQueue()

        self.input_device = None
        self.output_device = None
        self.dbus_interface = None

        self.isInCall = False

        self.volume = 0

        SAMPLERATE = 44100
        BLOCKSIZE = 1024
        CHANNEL = 1
        self.DTYPE = 'float32'

        self.audio_io_stream = sd.Stream(
            samplerate=SAMPLERATE,
            blocksize=BLOCKSIZE,
            dtype=self.DTYPE,
            channels=CHANNEL,
            callback=self.audio_io_callback
        )

        self.dbus_interface.on_incoming_audio(self.on_audio_packet_recvd)

    def start_stream(self):
        self.audio_io_stream.start()

    def audio_io_callback(self, indata, outdata, frames, time, status):
        self.volume = linalg.norm(indata)*10
        if self.dbus_interface is None:
            self.volume = 0
        self.input_buff.put_nowait(indata.tobytes())
        self.play_incoming_audio(outdata)

    def play_incoming_audio(self, outdata):
        try:
            pkt = self.input_buff.get_nowait()
            audio_data = frombuffer(pkt, self.DTYPE)
            audio_data = audio_data.reshape(outdata.shape)
            outdata[:] = audio_data 

        except Empty:
            outdata.fill(0)

        except ValueError:
            outdata.fill(0)

    async def dbus_worker(self):
        while True:
            loop = get_running_loop()
            try:
                data_b = await loop.run_in_executor(None, self.audio_buffer.get)
                await self.dbus_interface.call_send_audio_packet(data_b)
                sleep(0.5)

            except Exception as e:
                print(str(e))
                print_exc()

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

