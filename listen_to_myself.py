"""
Docstring for listen_to_myself

workflow:

i speak in mic => callback => playback

listen to myself type thing
"""
from time import sleep
import numpy as np
import sounddevice as sd
from queue import SimpleQueue, Empty
from asyncio import create_task

SAMPLERATE = 44100
BLOCKSIZE = 1024
CHANNEL = 1
DTYPE = 'float32'

inp_buf = SimpleQueue()

def output_callback(outdata):
    try:
        pkt = inp_buf.get_nowait()
        audio_data = np.frombuffer(pkt, DTYPE)
        audio_data = audio_data.reshape(outdata.shape)
        outdata[:] = audio_data 

    except Empty:
        outdata.fill(0)

    except ValueError:
        outdata.fill(0)

def input_audio_callback(indata, outdata, frames, time, status):
    inp_buf.put_nowait(indata.tobytes())
    output_callback(outdata)
    

in_stream = sd.Stream(
    samplerate=SAMPLERATE, 
    blocksize=BLOCKSIZE, 
    channels=CHANNEL,
    callback=input_audio_callback,
    dtype=DTYPE,
)

with in_stream:
    print("loopback running...")
    while True:
        sleep(1)