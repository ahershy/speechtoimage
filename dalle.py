#Requests allows you to send HTTP/1.1 requests easily
import requests
#This module provides functions for encoding binary data to printable ASCII characters and decoding such encodings back to binary data
import base64
#create web apps in python using streamlit
import streamlit as st

#This is the unique URL that obtained by going to the google colab link found in DALL-E Playground documentation and running the script to create the DALL-E mini server instance
URL = "https://sky-reservoir-fighting-sacrifice.trycloudflare.com"
headers = {'Bypass-Tunnel-Reminder': "go",
           'mode': 'no-cors'}

#Establishes connection to backend server and verifies it's valid
def check_if_valid_backend(url):
    try:
        resp = requests.get(url, timeout=5, headers=headers)
        return resp.status_code == 200
    except requests.exceptions.Timeout:
        return False
#Initiates call to server by sending text input for processing
def call_dalle(url, text, num_images=1):
    data = {"text": text, "num_images": num_images}
    resp = requests.post(url + "/dalle", headers=headers, json=data)
    if resp.status_code == 200:
        return resp
#Retrieves image json data, and decodes data using base64.b64decode()
def create_and_show_images(text, num_images):
    valid = check_if_valid_backend(URL)
    if not valid:
        st.write("Backend service is not running")
    else:
        resp = call_dalle(URL, text, num_images)
        if resp is not None:
            for data in resp.json():
                img_data = base64.b64decode(data)
                st.image(data)
