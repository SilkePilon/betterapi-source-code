import requests,sys,os
os.system("clear")
while True:
    message = input("> ")
    url = f"https://api.betterapi.net/youchat?inputs={message}&stream=True&key=site"

    with requests.get(url, stream=True) as r:
        for chunk in r.iter_content(1024):  # or, for line in r.iter_lines():
            sys.stdout.write(chunk.decode("latin1"))
            sys.stdout.flush()
        print("\n")