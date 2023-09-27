import requests

cookies = {
    'session-space-cookie': '902d66f16a7df3a391ba2fc1256d6eba',
    'hf-chat': '6190e238-397f-455a-ae2c-d70718f4a728',
    '_gid': 'GA1.2.521163100.1682860217',
    '__stripe_mid': '9e02ec0e-891c-4fb1-b04a-5083f27f20222ac9ce',
    'token': 'MeNDLPIZWiYZyAKvGnxLOSjzUHDSkdlUyCkwphmDwDZQWkpXkKPLlTGVwJpZgQpNiMMMNREmVrpAxadGolBAdcfcnsIPZnTkpjTEJgmPtBYkJsVnUazEzRoGLSpnssqf',
    '__stripe_sid': '69898a5b-88f9-4cca-b1a3-fd8d5593d816064f93',
    '_ga': 'GA1.1.1051370617.1682860053',
    '_ga_8Q63TH4CSL': 'GS1.1.1682869511.2.1.1682870710.0.0.0',
}

headers = {
    'authority': 'huggingface.co',
    'accept': '*/*',
    'accept-language': 'nl-NL,nl;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    # 'cookie': 'session-space-cookie=902d66f16a7df3a391ba2fc1256d6eba; hf-chat=6190e238-397f-455a-ae2c-d70718f4a728; _gid=GA1.2.521163100.1682860217; __stripe_mid=9e02ec0e-891c-4fb1-b04a-5083f27f20222ac9ce; token=MeNDLPIZWiYZyAKvGnxLOSjzUHDSkdlUyCkwphmDwDZQWkpXkKPLlTGVwJpZgQpNiMMMNREmVrpAxadGolBAdcfcnsIPZnTkpjTEJgmPtBYkJsVnUazEzRoGLSpnssqf; __stripe_sid=69898a5b-88f9-4cca-b1a3-fd8d5593d816064f93; _ga=GA1.1.1051370617.1682860053; _ga_8Q63TH4CSL=GS1.1.1682869511.2.1.1682870710.0.0.0',
    'dnt': '1',
    'origin': 'https://huggingface.co',
    'referer': 'https://huggingface.co/chat/conversation/644e91b7774f42958fde267b',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}

json_data = {
    'inputs': 'hi',
    'parameters': {
        'temperature': 0.9,
        'top_p': 0.95,
        'repetition_penalty': 1.2,
        'top_k': 50,
        'truncate': 1024,
        'watermark': False,
        'max_new_tokens': 200,
        'stop': [
            '</s>',
        ],
        'return_full_text': False,
    },
    'stream': True,
    'options': {
        'id': 'bd3776af-c4dd-419e-9921-345b792fe48b',
        'is_retry': False,
        'use_cache': False,
    },
}

response = requests.post(
    'https://huggingface.co/chat/conversation/644e91b7774f42958fde267b',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

print(response.text)