# main.py

from fastapi import FastAPI
import asyncio
import json
import os
import os, shutil
import platform
import re
import subprocess
import time
import urllib.parse
import uvicorn
import cloudscraper
from collections import OrderedDict
import markdownify
import undetected_chromedriver as uc
import urllib3
from pyvirtualdisplay import Display
from ratelimit import limits
from selenium.common import exceptions as SeleniumExceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import urllib.request
import numpy as np
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from gtts import gTTS
from bs4 import BeautifulSoup
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.requests import Request
from fastapi.responses import FileResponse
urllib3.disable_warnings()
from io import BytesIO
import string
from api_analytics.fastapi import Analytics
import traceback
import requests
import random
from fastapi import Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.responses import PlainTextResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import io
from starlette.responses import StreamingResponse
from PIL import Image
from typing import Optional, Any
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_queue import DistributedTaskApplyManager
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import collections.abc
from pptx import Presentation
from pptx.util import Inches
import aioredis
from fastapi.openapi.utils import get_openapi
from fastapi import Body
from fastapi.responses import StreamingResponse
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(debug=True)
redis = aioredis.Redis.from_url("redis://localhost")
origins = ["*"]
scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "android", "mobile": True,'desktop': False}, debug=False)


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"expected": "https://api.betterapi.net/youdotcom/chat?message=YOURMESSAGE&key=YOURKEY", "info": "more info and code can be found on the main page: https://betterapi.net/"}),
#     )


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=["*"],
)


# 805cf51e-db3f-4b04-9cce-8c73957ed177
app.add_middleware(Analytics, api_key="805cf51e-db3f-4b04-9cce-8c73957ed177")

app.mount("/about", StaticFiles(directory="static",html = True), name="static")

app.mount("/powerpointer", StaticFiles(directory="powerpoint",html = True), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/about/swagger-ui-bundle.js",
        swagger_css_url="/about/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/about/redoc.standalone.js",
    )



app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)








def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="BetterAPI",
        version="1.0.0",
        description="""Introducing BetterAPI: Access and Utilize You.com with Ease

BetterAPI is a free-to-use API designed to enhance your interaction with the You.com platform. With BetterAPI, you can seamlessly integrate YouChat into your projects and applications, providing a user-friendly and convenient way to leverage the capabilities of the chatbot.""",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    openapi_schema["paths"]["/youchat"]["get"]["x-codeSamples"] = [{
    'lang': 'Python',
    'source': """import requests # import requests for the api call

API_KEY = "YOUR KEY HERE" # your api key

url = "https://api.betterapi.net/youchat?inputs=hello&key=" + API_KEY # set api url
json = requests.get(url).json() # load json form api
print(json["generated_text"]) # print message response

""",
    'label': 'Python'
    }]
    
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


















def check_key(key): #needs an update
    if key == "site":
        return True
    if key == "xfrst":
        return True
    
    if key == "brave-bot-key_1l1b":
        return True

    with open("log.json", "r+") as TF:
        data = json.load(TF)
        data = str(data['users'].values())
        
        if key in data: 
            return True
        else:
            return False
        

global youchatapitimeout
youchatapitimeout = False






def get_response(success_status: bool, result: Any) -> JSONResponse | dict:
    if success_status:
        return JSONResponse(result, status_code=200)
    if result == -1:
        return JSONResponse(status_code=200, content={"message": "Im sorry, but we have reached the maximum number of users at the moment. Please wait a bit and try again later. Thank you for your patience!", "time": "01", "status_code": 200})
    else:
        return JSONResponse(status_code=500, content={"message": "Im sorry, but we have reached the maximum number of users at the moment. Please wait a bit and try again later. Thank you for your patience!", "time": "01", "status_code": 200})



async def chat_data_streamer(text):
    text = str(text['generated_text'])
    for i in text:
        yield str(i)
        time.sleep(0.01)



# @limits(calls=6, period=100)
@app.get("/youchat")
@limiter.limit("5/minute")
async def YouChat(request: Request,inputs,key,parameters:str = "", contextid = "", powerpointer = False,stream:bool=False):
    if check_key(key) == False:
        return {"error": "We apologize, but it appears that we were unable to locate a valid API key associated with this request. This issue may occur if you generated your key prior to February 26th, 2023. Please be advised that any API keys that have not been used within two hours of creation will automatically be deleted to ensure the security of our system. To resolve this issue, we recommend generating a new API key and ensuring that it is used within the designated time frame. Thank you for your understanding and cooperation."}
    # if key == "WS2VCRFW1JO9PBEHDGGT20WLVEJYSGQ9JYD":
    #     return "please stop with the model training or you will get ip banned"
    if "Generate a new dataset inspired by this one" in inputs:
        return "please stop with the model training or you will get ip banned"
    success_status: bool = False
    
    async with DistributedTaskApplyManager(
        redis = redis, 
        request_path = request.url.path,
        process_timeout = 45,
    ) as dtmanager:
        if not dtmanager.success():
            return JSONResponse(status_code=503, content={"generated_text": "Im sorry, but we have reached the maximum number of users at the moment. Please wait a bit and try again later. Thank you for your patience!", "time": "01", "status_code": 200})
        ip = request.headers.get("cf-connecting-ip")
        url = str(request.url)
        success_status, result = await dtmanager.rclt(form_data = {'inputs': inputs, 'parameters':parameters, 'contextid':contextid, 'ip':ip, 'url': url, "key":key, "powerpointer": powerpointer}, task_level = 0)
    if stream == True:
        return StreamingResponse(chat_data_streamer(result), media_type='text/event-stream')
    else:   
        return get_response(success_status, result)
        
 
@app.get("/youdotcom/chat")
async def new_endpoint():
    return "new endpoint! /youchat"        




# @limits(calls=6, period=100)
@app.post("/youchat")
@limiter.limit("10/minute")
async def YouChat(request: Request,inputs= Body(...), parameters= {}, contextid = "", powerpointer = False):
    # if key == "WS2VCRFW1JO9PBEHDGGT20WLVEJYSGQ9JYD":
    #     return "please stop with the model training or you will get ip banned"
    print(inputs)
    
    # inputs = json.loads(str(inputs))
    inputs = str(inputs['inputs'])
    print(type(inputs))
    success_status: bool = False
    
    async with DistributedTaskApplyManager(
        redis = redis, 
        request_path = request.url.path,
        process_timeout = 45,
    ) as dtmanager:
        if not dtmanager.success():
            return JSONResponse(status_code=503, content={"generated_text": "Im sorry, but we have reached the maximum number of users at the moment. Please wait a bit and try again later. Thank you for your patience!", "time": "01", "status_code": 200})
        ip = request.headers.get("cf-connecting-ip")
        url = str(request.url)
        success_status, result = await dtmanager.rclt(form_data = {'inputs': inputs, 'parameters':parameters, 'contextid':contextid, 'ip':ip, 'url': url,"powerpointer": powerpointer, "key": "site"}, task_level = 0)
        print(result)
    return Response(content=str(result), media_type='text/event-stream')
        
        
            # if message == "":
            #     return {"error": "message not defined"}
            # if request.headers.get("referer") == "https://api.betterapi.net/about/":
            #     data = sendmessagetochat(message,contextid, request)
            #     return data
            # if check_key(key) == False:
            #     return {"error": "no valid api key was found!"}
            # data = sendmessagetochat(message,contextid, request)
            # return JSONResponse(content=data)



# @limits(calls=6, period=100)
@app.get("/betterapi/betterchat")
@limiter.limit("15/minute")
async def BetterChat(request: Request,message,key, contextid = "", powerpointer = False):
    if check_key(key) == False:
        return {"error": "We apologize, but it appears that we were unable to locate a valid API key associated with this request. This issue may occur if you generated your key prior to February 26th, 2023. Please be advised that any API keys that have not been used within two hours of creation will automatically be deleted to ensure the security of our system. To resolve this issue, we recommend generating a new API key and ensuring that it is used within the designated time frame. Thank you for your understanding and cooperation."}
    success_status: bool = False
    
    async with DistributedTaskApplyManager(
        redis = redis, 
        request_path = request.url.path,
        process_timeout = 45,
    ) as dtmanager:
        if not dtmanager.success():
            return JSONResponse(status_code=503, content='{"message": "Im sorry, but we have reached the maximum number of users at the moment. Please wait a bit and try again later. Thank you for your patience!", "time": "01", "status_code": 200}')
        ip = request.headers.get("cf-connecting-ip")
        url = str(request.url)
        success_status, result = await dtmanager.rclt(form_data = {'message': message, 'contextid':contextid, 'ip':ip, 'url': url, "key":key, "powerpointer": powerpointer}, task_level = 0)
    return get_response(success_status, result)



# @limits(calls=6, period=100)
@app.get("/google/bard")
@limiter.limit("10/minute")
async def Google_Bard(request: Request,message,key, contextid = "", powerpointer = False):
    if check_key(key) == False:
        return {"error": "We apologize, but it appears that we were unable to locate a valid API key associated with this request. This issue may occur if you generated your key prior to February 26th, 2023. Please be advised that any API keys that have not been used within two hours of creation will automatically be deleted to ensure the security of our system. To resolve this issue, we recommend generating a new API key and ensuring that it is used within the designated time frame. Thank you for your understanding and cooperation."}
    success_status: bool = False
    
    async with DistributedTaskApplyManager(
        redis = redis, 
        request_path = request.url.path,
        process_timeout = 45,
    ) as dtmanager:
        if not dtmanager.success():
            return JSONResponse(status_code=503, content='{"message": "Im sorry, but we have reached the maximum number of users at the moment. Please wait a bit and try again later. Thank you for your patience!", "time": "01", "status_code": 200}')
        ip = request.headers.get("cf-connecting-ip")
        url = str(request.url)
        success_status, result = await dtmanager.rclt(form_data = {'message': message, 'contextid':contextid, 'ip':ip, 'url': url, "key":key, "powerpointer": powerpointer}, task_level = 0)
    return get_response(success_status, result)





# @limits(calls=6, period=100)
@app.get("/imagine/gen")
@limiter.limit("3/minute")
async def Stable_Diffusion(request: Request,prompt,key,style:int = 78):
    if check_key(key) == False:
        return {"error": "We apologize, but it appears that we were unable to locate a valid API key associated with this request. This issue may occur if you generated your key prior to February 26th, 2023. Please be advised that any API keys that have not been used within two hours of creation will automatically be deleted to ensure the security of our system. To resolve this issue, we recommend generating a new API key and ensuring that it is used within the designated time frame. Thank you for your understanding and cooperation."}
    success_status: bool = False
    
    # prompt = str(prompt).encode('utf-8')
    
    async with DistributedTaskApplyManager(
        redis = redis, 
        request_path = request.url.path,
        process_timeout = 200,
    ) as dtmanager:
        if not dtmanager.success():
            return JSONResponse(status_code=503, content="Service Temporarily Unavailable, please note that the api is still in dev.")
        ip = request.headers.get("cf-connecting-ip")
        print(ip)
        url = str(request.url)
        success_status, result = await dtmanager.rclt(form_data = {'prompt': prompt, 'ip':ip, 'url': url, 'key': key, 'style':style}, task_level = 0)
    return JSONResponse(result, status_code=200)


@app.get("/generated/{id}/{name}")
@limiter.limit("5/minute")
async def image_endpoint(id: str,name: str,request: Request):
    path = str(request.url).replace("api.betterapi.net", "images.wombo.art").replace("http", "https")
    print(path)
    with open(f'downloads/{id}.png', 'wb') as handle:
        response = requests.get(path, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
    return FileResponse(f'downloads/{id}.png')

# @limits(calls=6, period=100)
@app.get("/youdotcom/apps")
@limiter.limit("15/minute")
async def You_Apps(request: Request,search,key, appname = ""):
    if check_key(key) == False:
        return {"error": "We apologize, but it appears that we were unable to locate a valid API key associated with this request. This issue may occur if you generated your key prior to February 26th, 2023. Please be advised that any API keys that have not been used within two hours of creation will automatically be deleted to ensure the security of our system. To resolve this issue, we recommend generating a new API key and ensuring that it is used within the designated time frame. Thank you for your understanding and cooperation."}
    success_status: bool = False
    
    async with DistributedTaskApplyManager(
        redis = redis, 
        request_path = request.url.path,
        process_timeout = 45,
    ) as dtmanager:
        if not dtmanager.success():
            return JSONResponse(status_code=503, content="Service Temporarily Unavailable, please note that the api is still in dev.")
        ip = request.headers.get("cf-connecting-ip")
        url = str(request.url)
        success_status, result = await dtmanager.rclt(form_data = {'message': search, 'app_name':appname, 'ip':ip, 'url': url, "key":key}, task_level = 0)
    return get_response(success_status, result)

# @limits(calls=6, period=100)
@app.get("/youdotcom/history")
@limiter.limit("10/minute")
async def history_out_of_date(request: Request, key):
    with open("log.json",'r') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            try:
                history = file_data["users"][f"{key}"]["chat_history"]
            except:
                return {"error": "We apologize, but it appears that we were unable to locate a valid API key associated with this request. This issue may occur if you generated your key prior to Match 1, 2023. Please be advised that any API keys that have not been used within two hours of creation will automatically be deleted to ensure the security of our system. To resolve this issue, we recommend generating a new API key and ensuring that it is used within the designated time frame. Thank you for your understanding and cooperation."}
    return {"history": f"{history}"}


# @limits(calls=6, period=100)
@app.get("/gen")
@limiter.limit("10/minute")
async def Key_gen(request: Request):
        
    ip = request.headers.get("cf-connecting-ip")
    with open("log.json",'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        try:
            key = file_data["users"][f"{ip}"]["key"]
            return {"key": f"{key}"}
        except:
            new_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(35))
            file_data['users'].update({ip: {"key":new_key, "chat_history": []}})
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
            return {"key": f"{new_key}"}
        
        
# @limits(calls=6, period=100)
@app.get("/youdocom/osapi")
@limiter.limit("10/minute")
async def osapi_for_you_dot_com(request: Request):
    
    wiki_data = requests.get("https://en.wikipedia.org/wiki/List_of_Linux_distributions").text
    soup = BeautifulSoup(wiki_data, 'html.parser')
    os = soup.find_all('table', {'class' : 'wikitable'})
    os_list = []
    for oss in os:
        info = oss.find_all("a")
        for a in info:
            print(a)
            os_list.append({'title':a.get("title"), 'link': a.get("href")})
        
    
    # table_data = [[cell.text for cell in row("td")]
    #                      for row in BeautifulSoup(wiki_data)("tr")]
    # return json.dumps(OrderedDict(table_data))
    return os_list

# @limits(calls=6, period=100)




# @limits(calls=6, period=100)
@app.get("/youdotcom/cts")
@limiter.limit("5/minute")
async def YouChat_Text_To_Speach_out_of_date(request: Request,message,key,contextid = ""):
    if check_key(key) == False:
        return {"error": "We apologize, but it appears that we were unable to locate a valid API key associated with this request. This issue may occur if you generated your key prior to Match 1, 2023. Please be advised that any API keys that have not been used within two hours of creation will automatically be deleted to ensure the security of our system. To resolve this issue, we recommend generating a new API key and ensuring that it is used within the designated time frame. Thank you for your understanding and cooperation."}
    success_status: bool = False
    
    async with DistributedTaskApplyManager(
        redis = redis, 
        request_path = "/youdotcom/chat",
        process_timeout = 45,
    ) as dtmanager:
        if not dtmanager.success():
            return JSONResponse(status_code=503, content="Service Temporarily Unavailable, please note that the api is still in dev.")
        ip = request.headers.get("cf-connecting-ip")
        url = str(request.url)
        success_status, result = await dtmanager.rclt(form_data = {'message': message, 'contextid':contextid, 'ip':ip, 'url': url}, task_level = 0)
    chatstr = result['message']
    tts = gTTS(f'{chatstr}')
    file_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    tts.save(f'mp3/{file_name}.mp3')
    return FileResponse(f"mp3/{file_name}.mp3")

# # @limits(calls=6, period=100)
# @app.get("/")
# async def root(request: Request):
#     return PlainTextResponse("""
# Welcome to the YouDotCom Python library! Our library now features an easy-to-use public API that allows you to interact with YouChat. With this API, you can easily integrate YouChat into your own projects and applications, providing a convenient and user-friendly way for your users to access and utilize the capabilities of the chat bot.


# base url: api.betterapi.net

# To send a message to YouChat and receive a JSON response, you can make an HTTP GET request to the endpoint /youdotcom/chat, including the message to be sent as a query parameter. The key is message and the value should be the message text encoded in URL format. For example, to send the message hello there, the endpoint would be /youdotcom/chat?message=hello%20there. The JSON response will include the message sent by YouChat, time, v2Captcha, and type of the request.

# Another endpoint is provided to convert the output text into speech, the endpoint is /youdotcom/cts. The message to be converted should be included as a query parameter in the URL, with the key message and the value being the message text. For example, to convert the message hello there into speech, the endpoint would be /youdotcom/cts?message=hello%20there


# We are constantly improving and updating the YouDotCom library and API, so make sure to check back for new features and updates. If you have any questions or need assistance, feel free to reach out in the Discusions tab on github. I'm always happy to help.

# For more info: https://github.com/You-OpenSource/You-Python/blob/main/README.md#api
# """)

# RedirectResponse(url='/')
from fastapi.responses import HTMLResponse
@app.get("/status", response_class=HTMLResponse)
async def read_items():
    html_content = """
    <html>
        <head>
            <title>Status</title>
        </head>
        <body>
            <iframe src="https://my-api-analytics.vercel.app/dashboard/295369d573eb4cb99e82857f07390675" style="position:fixed; top:0; left:0; bottom:0; right:0; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden; z-index:999999;">Your browser doesn't support iframes
            </iframe>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/")
async def about(request: Request):
    return RedirectResponse(url='/about')


@app.get("/betterchat")
async def BetterChat_webui():
    
    htmlcode = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>BetterChat</title>
  </head>
  <body>
	<iframe src="https://betterapi-betterchat.hf.space" frameborder="0" style="position:fixed; top:0; left:0; bottom:0; right:0; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden; z-index:999999;" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
  </body>
</html>
"""
    
    return HTMLResponse(content=htmlcode, status_code=200)

@app.get('/GeneratedPresentations/')
def send_generated_ppt(path):
    file_path = f'GeneratedPresentations/{path}'
    headers = {
        "Content-Disposition": f"attachment; filename={path}"
    }
    return FileResponse(file_path, headers=headers)

@app.get('/powerpointer/GeneratedPresentations/')
def send_generated_ppt2(path):
    file_path = f'GeneratedPresentations/{path}'
    headers = {
        "Content-Disposition": f"attachment; filename={path}"
    }
    return FileResponse(file_path, headers=headers)

@limiter.limit("1/minute")
@app.get("/powerget")
async def powerget(request: Request,msg):
    success_status: bool = False
    
    async with DistributedTaskApplyManager(
        redis = redis, 
        request_path = "/powerget",
        process_timeout = 35,
    ) as dtmanager:
        if not dtmanager.success():
            return JSONResponse(status_code=503, content="Service Temporarily Unavailable, please note that the api is still in dev.")
        ip = request.headers.get("cf-connecting-ip")
        url = str(request.url)
        success_status, result = await dtmanager.rclt(form_data = {'msg': msg}, task_level = 0)
    return result
    
    

if __name__ == "__main__":
    try:
        uvicorn.run(app,host="192.168.2.94",port=80)
    except:
        print(traceback.format_exc())
