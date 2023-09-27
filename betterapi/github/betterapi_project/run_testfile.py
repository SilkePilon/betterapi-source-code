# main.py

from fastapi import FastAPI
from youdotcom import Chat
import asyncio
import json
import os
import platform
import re
import subprocess
import time
import urllib.parse
import uvicorn
import chromedriver_autoinstaller
import cloudscraper
import markdownify
import undetected_chromedriver.v2 as uc
import urllib3
from pyvirtualdisplay import Display
from ratelimit import limits
from selenium.common import exceptions as SeleniumExceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from gtts import gTTS
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.requests import Request
from fastapi.responses import FileResponse
urllib3.disable_warnings()
import string
from api_analytics.fastapi import Analytics
import traceback
import random
from youdotcom import Webdriver
from starlette.responses import PlainTextResponse, RedirectResponse
driver = Webdriver(webdriver_path="/betterapi/usr/bin/chromedriver", hide=True, headless=True).driver
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 805cf51e-db3f-4b04-9cce-8c73957ed177
# app.add_middleware(Analytics)

app.mount("/betterapi/about", StaticFiles(directory="static",html = True), name="static")


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def check_key(key):
    if key == "": 
        return False
    with open("payed_api_keys.txt", "r") as f:
        keys = f.readlines()
    for keystr in keys:
        if key in keystr:
            return True
    with open("api_keys.txt", "r") as f:
        keys = f.readlines()
    for keystr in keys:
        if key in keystr:
            return True
    else:
        return False


def sendmessagetochat(message, request):
    try:
        with open("logs.txt", "a+") as T:
            ip = request.headers.get("cf-connecting-ip")
            datetimestr = datetime.today()
            T.write(f"{ip} @ {datetimestr} @{request.url}\n")
        start = time.time()
        scraper = cloudscraper.create_scraper(browser={"browser": "firefox", "platform": "windows", "mobile": False}, debug=False)
        CloudflareChallengeError = False
        typeof = ""

        

        global chat
        chat = []
        headers = {
            "Accept": "text/event-stream",
            "Connection": "keep-alive",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
            "Referer": "https://you.com/search?q=hello&fromSearchBar=true&tbm=youchat",
            "Cookie": b"uuid_guest=dummystring;",
        }
        payload = {
            "q": message,
            "chat": "",
            "queryTraceId": "",
            "domain": "youchat",
            "page": "1",
            "count": "10",
            "safeSearch": "Off",
            "onShoppingPage": "false",
            "freshness": "Month",
            "mkt": "",
            "responseFilter": "WebPages,Translations,TimeZone,Computation,RelatedSearches",
        }
        try:
            response = scraper.get(f"https://you.com/api/streamingSearch", params=payload, headers=headers)
            CloudflareChallengeError = False
            typeof = "api"
            
        except cloudscraper.exceptions.CloudflareChallengeError as e:
            driver.get(f"https://you.com/api/streamingSearch?q={message}&page=1&count=10&safeSearch=Moderate&onShoppingPage=false&mkt=&responseFilter=WebPages,Translations,TimeZone,Computation,RelatedSearches&domain=youchat&queryTraceId=&chat={str(chat)}")
            driver.add_cookie({'name' : 'uuid_guest', 'value' : 'dummystring'})
            CloudflareChallengeError = True
            typeof = "webdriver"
            response = driver.page_source.split("\n")
        
            
            
            
        output = ""
        if CloudflareChallengeError == True:
            for line in response:
                if line:
                    decoded_line = str(line)
                    key, value = decoded_line.split(":", 1)
                    key = key.strip()
                    value = value.strip()
                    if key == "data":
                        if value == "I'm Mr. Meeseeks. Look at me.":
                            break
                        data = json.loads(value)
                        if "youChatToken" in data:
                            output += data["youChatToken"]
        if CloudflareChallengeError == False:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    key, value = decoded_line.split(":", 1)
                    key = key.strip()
                    value = value.strip()
                    if key == "data":
                        if value == "I'm Mr. Meeseeks. Look at me.":
                            break
                        data = json.loads(value)
                        if "youChatToken" in data:
                            output += data["youChatToken"]
        if len(chat) > 4:
            chat = chat[:-4]

        # print(chat)

        out = re.sub(r"\[.+?\]\(.+?\)", "", output[1:])
        # out = out[1:]
        msg = markdownify.markdownify(out)

        # subprocess.call(["taskkill", "/betterapi/im", "chromedriver.exe"],shell=True)
        # subprocess.call(["pkill", "-f", "chromedriver"], shell=True)
        # subprocess.call(["killall", "-m", "chromedriver"], shell=True)
        timedate = time.time() - start
        timedate = time.strftime("%S", time.gmtime(timedate))

        return {"message": msg, "time": str(timedate), "v2Captcha": str(CloudflareChallengeError), "type": str(typeof)}
    except: 
        print(traceback.format_exc())



# @limits(calls=6, period=100)
@app.get("/betterapi/betterapi/youdotcom/chat")
@limiter.limit("5/betterapi/minute")
async def YouChat(request: Request,message,key):
    
    if message == "":
        return {"error": "message not defined"}
    if request.headers.get("referer") == "https://api.betterapi.net/about/":
        data = sendmessagetochat(message, request)
        return data
    if check_key(key) == False:
        return {"error": "no valid api key was found!"}
    data = sendmessagetochat(message, request)
    return data
    


# @limits(calls=6, period=100)
@app.get("/betterapi/betterapi/gen")
@limiter.limit("10/betterapi/minute")
async def Key_gen(request: Request):
    with open("api_keys.txt", "r") as f:
        keys = f.readlines()
        for key in keys:
            ip, keystring = key.split("||")
            if ip == request.headers.get("cf-connecting-ip"):
                return {"key": f"{keystring}"}
    
    
    new_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(35))
    print(new_key)
    
    with open("api_keys.txt", "a+") as F:
        ip = request.headers.get("cf-connecting-ip")
        F.write(f"{ip}||{new_key}\n")
    return {"key": f"{new_key}"}

# @limits(calls=6, period=100)




# @limits(calls=6, period=100)
@app.get("/betterapi/betterapi/youdotcom/cts")
@limiter.limit("5/betterapi/minute")
async def YouCHatTextToSpeach(request: Request,message,key):
    if message == "":
        return {"error": "message not defined"}
    if check_key(key) == False:
        return {"error": "no valid api key was found!"}
    chatstr = sendmessagetochat(message, request)
    chatstr = chatstr['message']
    tts = gTTS(f'{chatstr}')
    file_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    tts.save(f'mp3/{file_name}.mp3')
    return FileResponse(f"mp3/{file_name}.mp3")

# # @limits(calls=6, period=100)
# @app.get("/betterapi/betterapi/")
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
@app.get("/betterapi/betterapi/status", response_class=HTMLResponse)
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

@app.get("/betterapi/betterapi/")
async def about(request: Request):
    return RedirectResponse(url='/about')

if __name__ == "__main__":
    try:
        uvicorn.run(app,host="192.168.2.88",port=80)
    except:
        print(traceback.format_exc())