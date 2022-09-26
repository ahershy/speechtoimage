#create web apps in python using streamlit
import streamlit as st
#PyAudio provides Python bindings for PortAudio v19, the cross-platform audio I/O library. Allows computer mic to work with python
import pyaudio
#python library for building a websocket server, a two-way interactive communication session between the user's browser and a server.
import websockets
#asyncio is a library to write concurrent code using the async/await syntax.
import asyncio
#This module provides functions for encoding binary data to printable ASCII characters and decoding such encodings back to binary data
import base64
#Python has a built-in package called json, which can be used to work with JSON data.
import json
#pulling in the api key for AssemblyAI
from configure import api_key
#pulling in function from other file
from dalle import create_and_show_images

#configuring session_state
if 'text' not in st.session_state:
    st.session_state['text'] = ''
    st.session_state['run'] = False

#creating webapp title
st.title("DALL-E Mini")

#function to begin session_state
def start_listening():
    st.session_state["run"] = True

#button to activate session_state function
st.button("Say something", on_click=start_listening)

#text on application
text = st.text_input("What should I create?", value=st.session_state["text"])

#slider visualization
num_images = st.slider("How many images?", 1, 6)

#variable for button
ok = st.button("GO!")

#if statement to determine when to call and retreive from dalle file
if ok and text:
    create_and_show_images(text, num_images)

# the AssemblyAI endpoint we're going to hit
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

#setting up microphone paramaters
#how many bytes of data per chunk of audio processed
FRAMES_PER_BUFFER = 3200
#port audio input / output bit integer format, this is default
FORMAT = pyaudio.paInt16
#monoformat channel, meaning we only need the input audio coming from 1 direction
CHANNELS = 1
#desired rate in Hz of incoming audio
RATE = 16000
p = pyaudio.PyAudio()

# starts recording, creating stream variable, assigning paramaters
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)
#creating asynchronous function, so it can continue running and sending stream of speech data to API for as long as is needed
async def send_receive():
    print(f'Connecting websocket to url ${URL}')

    async with websockets.connect(
		URL,
		extra_headers=(("Authorization", api_key),),
		ping_interval=5,
		ping_timeout=20
	) as _ws:

        r = await asyncio.sleep(0.1)
        print("Receiving Session begins ...")

        session_begins = await _ws.recv()

        async def send():
            while st.session_state['run']:
                try:
                    data = stream.read(FRAMES_PER_BUFFER)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data":str(data)})
                    r = await _ws.send(json_data)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    print(e)
                    assert False, "Not a websocket 4008 error"

                r = await asyncio.sleep(0.01)


        async def receive():
            while st.session_state['run']:
                try:
                    result_str = await _ws.recv()
                    result = json.loads(result_str)['text']

                    if json.loads(result_str)['message_type'] == 'FinalTranscript':
                        result = result.replace('.', '')
                        result = result.replace('!', '')
                        st.session_state['text'] = result
                        st.session_state['run'] = False
                        st.experimental_rerun()
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    print(e)
                    assert False, "Not a websocket 4008 error"

        send_result, receive_result = await asyncio.gather(send(), receive())


asyncio.run(send_receive())
