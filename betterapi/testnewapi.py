import requests

proxy = "socks5://localhost:7890"
resp = requests.post("http://localhost:8000/challenge",
                     json={"proxy": {"server": proxy}, "timeout": 20,
                           "url": "https://nowsecure.nl"})
if resp.json().get("success"):
    ua = resp.json().get("user_agent")
    cf_clearance_value = resp.json().get("cookies").get("cf_clearance")
    # use cf_clearance, must be same IP and UA
    headers = {"user-agent": ua}
    cookies = {"cf_clearance": cf_clearance_value}
    res = requests.get('https://nowsecure.nl', proxies={
        "all": proxy
    }, headers=headers, cookies=cookies)
    if '<title>Just a moment...</title>' not in res.text:
        print("cf challenge success")