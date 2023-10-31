import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime
import sys

load_dotenv()

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
}

def baseDaily(reqUrl,payload,headers):
    if not payload.get("act_id"):
        print("[-] act_id not found")
        sys.exit()
    
    if not headers.get('Cookie'):
        print("[-] cookie not found")
        sys.exit()

    response = requests.post(reqUrl, data=payload,  headers=headers)
    return response.json()
    


def honkaiDaily():
    print("Daily Signin Honkai StarRail:")

    reqUrl = "https://sg-public-api.hoyolab.com/event/luna/os/sign"
    cookie = os.getenv("Cookie") if os.getenv("SameAccount") else os.getenv("HonkaiCookie")

    payload = {
        "act_id": os.getenv("HonkaiActId"),
        "lang": "en-us"
    }

    headers["Cookie"] = cookie

    response = baseDaily(reqUrl,payload,headers)

    print(response['message'],end="\n\n")


def genshinDaily():
    print("Daily Signin Genshin Impact:")
    reqUrl = "https://sg-hk4e-api.hoyolab.com/event/sol/sign?lang=en-us"
    cookie = os.getenv("Cookie") if os.getenv("SameAccount") else os.getenv("GenshinCookie")
    payload = {
        "act_id": os.getenv("GenshinActId"),
        "lang": "en-us"
    }

    headers["Cookie"] = cookie

    response = baseDaily(reqUrl,payload, headers)

    print(response['message'],end="\n\n")

if __name__ == '__main__':
    dateFile = "date.txt"
    dateToday = datetime.now().strftime("%D")

    if os.path.exists(dateFile):
        with open(dateFile) as f:
            prevdate = f.read()
            if prevdate == dateToday:
                print("Already Logged In")
                sys.exit()
    try:
        honkaiDaily()
        genshinDaily()
        dateToday = datetime.now().strftime("%D")
        with open(dateFile,"w") as f:
            f.write(dateToday)
    except Exception as e:
        print(f"Error Occured: {e}")