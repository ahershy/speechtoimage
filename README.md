# speech to image

# Background knowledge needed:
DALL-E was created by the organization OpenAI. This introduced the world to AI generated images and took off in popularity about a year ago. 
DALL-E mini is an open source alternative to DALL-E that tinkerers, like you and I, can play around with for free. This is the engine we'll be leveraging in this tutorial
DALL-E Playground is an open source application that does two things: 1. Uses Google Colab to create and run a backend DALL-E mini server which provides the GPU processing needed to generate images. And 2. Provides a front-end web interface via javascript that users can interact with and view their images on.

# What this application does:
Reengineers DALL-E Playground's front-end interface from javascript to streamlit python (because 1. The UI looks better 2. It functions more seamlessly with the speech to text API and 3. Python is cooler). 
Leverages AssemblyAI's speech to text API to transcribe speech into the text input DALL-E mini engine can work with
Listens to speech and displays creative and interesting images 

# Design
This project is broken up into two primary files: main.py and dalle.py.
The 'main' script is used for both the streamlit web application and the voice-to-text API connection. It involves configuring the streamlit session-state, creating a visual features such as buttons and sliders on the web app, setting up a WebSockets server, filling in all the parameters required for pyaudio, creating asynchronous functions for sending and receiving the speech data concurrently between our application and the AssemblyAi's server.
The dalle.py file is used to connect the streamlit web application to the Google Colab server running the DALL-E mini engine. This file has a few functions which serve the following purposes: 
Establishes connection to backend server and verifies it's valid
Initiates call to server by sending text input for processing 
Retrieves image json data, and decodes data using base64.b64decode()

This project is heavily influenced by https://www.youtube.com/watch?v=fRa2rmDvOCY&t=412s&ab_channel=AssemblyAI
