from asyncio import create_task
import sounddevice as sd
from threading import Thread
from client_utils import ClientDBUS

class ThreadedAudioService:
    def __init__(self):
        super(ThreadedAudioService, self).__init__()
        
        self.dbus = ClientDBUS()

        create_task(self.dbus.setup())

        self.stream = sd.InputStream(
            samplerate=44100,
            blocksize=1024,
            callback=self.callback
        )

        self.interface = self.dbus.get_interface()
        self.thread = Thread(target=self.stream.start, daemon=True)

    async def callback(self, indata, frames, time, status):
        await self.interface.call_send_audio_packet(indata.tobytes())
