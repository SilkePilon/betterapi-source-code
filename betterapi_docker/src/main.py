# main.py

from fastapi import FastAPI
import asyncio
import json
import os
import platform
import re
import subprocess
import time
import urllib.parse
import uvicorn
import cloudscraper
import markdownify
import undetected_chromedriver as uc
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
from io import BytesIO
import string
from api_analytics.fastapi import Analytics
import traceback
import requests
import random
from fastapi import Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from youdotcom import Webdriver
from starlette.responses import PlainTextResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
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
import aioredis
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()


subprocess.Popen(["python","redis_main.py",f"{sys.argv[1]}"])


time.sleep(10)




redis = aioredis.Redis.from_url("redis://localhost")
origins = ["*"]
scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "android", "mobile": True,'desktop': False}, debug=False)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"expected": "https://api.betterapi.net/youdotcom/chat?message=YOURMESSAGE&key=YOURKEY", "info": "more info and code can be found on the main page: https://betterapi.net/"}),
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 805cf51e-db3f-4b04-9cce-8c73957ed177
app.add_middleware(Analytics, api_key="805cf51e-db3f-4b04-9cce-8c73957ed177")

app.mount("/about", StaticFiles(directory="static",html = True), name="static")


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

global youchatapitimeout
youchatapitimeout = False


def get_response(success_status: bool, result: Any) -> JSONResponse | dict:
    if success_status:
        return result
    if result == -1:
        return JSONResponse(status_code=503, content=f"Service Temporarily Unavailable")
    else:
        return JSONResponse(status_code=500, content=f"Internal Server Error")





# @limits(calls=6, period=100)
@app.get("/youdotcom/chat")
@limiter.limit("15/minute")
async def YouChat(request: Request,message,key, contextid = ""):
    success_status: bool = False
    
    async with DistributedTaskApplyManager(
        redis = redis, 
        request_path = request.url.path,
    ) as dtmanager:
        if not dtmanager.success():
            return JSONResponse(status_code=503, content="Service Temporarily Unavailable, please note that the api is still in dev.")
        ip = request.headers.get("cf-connecting-ip")
        url = str(request.url)
        success_status, result = await dtmanager.rclt(form_data = {'message': message, 'contextid':contextid, 'ip':ip, 'url': url}, task_level = 0)
    return get_response(success_status, result)
        
        
        
        
@app.get("/youdotcom/draw")
@limiter.limit("100/minute")
async def YouChat(request: Request,message,key):
    
    if message == "":
        return {"error": "message not defined"}
    if request.headers.get("referer") == "https://api.betterapi.net/about/":
        data = stable_defusion(message, request)
        return data
    if check_key(key) == False:
        return {"error": "no valid api key was found!"}
    data = stable_defusion(message, request)
    return JSONResponse(content=data)

    


# @limits(calls=6, period=100)
@app.get("/gen")
@limiter.limit("10/minute")
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
@app.get("/youdotcom/cts")
@limiter.limit("5/minute")
async def YouCHatTextToSpeach(request: Request,message,key,contextid = ""):
    if message == "":
        return {"error": "message not defined"}
    if check_key(key) == False:
        return {"error": "no valid api key was found!"}
    chatstr = sendmessagetochat(message,contextid, request)
    chatstr = chatstr['message']
    tts = gTTS(f'{chatstr}')
    file_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    tts.save(f'mp3/{file_name}.mp3')
    return FileResponse(f"mp3/{file_name}.mp3")


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

if __name__ == "__main__":
    try:
        uvicorn.run(app,host="0.0.0.0",port=80)
    except:
        print(traceback.format_exc())
