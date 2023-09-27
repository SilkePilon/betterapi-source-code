import gradio as gr
import requests
from PIL import Image
import requests
from io import BytesIO
import urllib.parse

def youchat(x):
    x = urllib.parse.quote(x)
    url = f"https://api.betterapi.net/youdotcom/chat?message={x}&key=site"
    url2 = f"https://api.betterapi.net/youdotcom/chat?message={x}&key=YOUR_KEY_HERE"
    data = requests.get(url).json()
    message = data['message']
    time = data['time']
    return message, time, url2, data

def imagine(x, y):
    x = urllib.parse.quote(x)
    url = f"https://api.betterapi.net/youdotcom/imagine?message={x}&model={y}&key=site"
    url2 = f"https://api.betterapi.net/youdotcom/imagine?message={x}&model={y}&key=YOUR_KEY_HERE"
    data = requests.get(url).json()
    try:
        image = data['image_url']
    except:
        image = "error"
    if not "https://" in image:
        response = requests.get("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEtyeBWNAjbbldUl1z35F7KwgwBK9jlqliQQ&usqp=CAU")
        img = Image.open(BytesIO(response.content))
    else:
        response = requests.get(image)
        img = Image.open(BytesIO(response.content))
        
    return img, data, url2

with gr.Blocks() as demo:
    gr.Markdown("Try out BetterAPI!")
    with gr.Tab("YouChat"):
        text_input = gr.Textbox(label="Input", placeholder="Message to YouChat")
        text_output = gr.Textbox(label="Response", placeholder="Message from YouChat")
        time_taken = gr.Number(label="Time taken (server side)")
        url_output = gr.Textbox(label="Request URL", placeholder="url for api")
        raw_output = gr.Textbox(label="Raw data", placeholder="Raw data form api")
        text_button = gr.Button("Chat!")
    with gr.Tab("Imagine"):
        with gr.Row():
            image_output = gr.Image(shape=[100, 100])
        image_input = gr.Textbox(label="Promt", placeholder="Describe the image to be created")
        model_input = gr.Dropdown(["stable-diffusion", "stable-diffusion-v2.1", "openjourney", "anime"], label="Choose a model")
        raw_output2 = gr.Textbox(label="Raw data", placeholder="Raw data form api")
        url_output2 = gr.Textbox(label="Request URL", placeholder="url for api")
        image_button = gr.Button("Genarate!")

    with gr.Accordion("API docs"):
        gr.Markdown("""
To get started, you will first need to get an API key on our website. This key will be required to authenticate each API request.

base url: api.betterapi.net

To send a message to YouChat and receive a JSON response, you can make an HTTP GET request to the endpoint /youdotcom/chat, including the message to be sent as a query parameter. The key is message and the value should be the message text encoded in URL format. For example, to send the message hello there, the endpoint would be https://api.betterapi.net/youdotcom/chat?message=hello%20there&key=YOUR_API_KEY. The JSON response will include the message sent by YouChat, time, v2Captcha, and type of the request.

You also need to set your API key, you can do this by providing it as an parameter like this /youdotcom/chat?message=hello%20there&key=YOUR_API_KEY

auto updating docs can be found at: https://betterapi.net/redoc

Make sure to include the API key in the url of each request to authenticate it.

We are constantly improving and updating the YouDotCom library and API, so make sure to check back for new features and updates. If you have any questions or need assistance, feel free to reach out in the Discusions tab. I'm always happy to help.
""")

    text_button.click(youchat, inputs=text_input, outputs=[text_output, time_taken, url_output, raw_output])
    image_button.click(imagine, inputs=[image_input, model_input], outputs=[image_output, raw_output2, url_output2])

demo.launch(server_name="192.168.2.94")