import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime
import sys
import shutil
from constants import urls
from discord import SyncWebhook,Embed




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

    response = requests.post(reqUrl, data=json.dumps(payload),  headers=headers)
    return response
    


def daily_login(games):
    for game in games:
        print(f"{urls[game]['title']}:")

        reqUrl = urls[game]['signUrl']
        infoUrl = urls[game]['infoUrl']
        rewardUrl = urls[game]['rewardsUrl']
        cookie = getenv("Cookie") if getenv("SameAccount") else getenv(f"{game.capitalize()}Cookie")

        payload = {
            "act_id": urls[game]['act_id'],
            "lang": "en-us"
        }

        headers["Cookie"] = cookie
        response = baseDaily(reqUrl,payload,headers)
        writeLog(os.path.join(logDir,f"{game}.txt"),response.json())

        infoResp = requests.get(infoUrl,headers=headers)
        total_days = infoResp.json()['data']['total_sign_day']

        rewardResp = requests.get(rewardUrl,headers=headers)
        today_reward = rewardResp.json()['data']['awards'][total_days-1]

        sendDiscordMessage(response.json()['message'],today_reward,total_days,game=game)
        print(f"{response.json()['message']}: {today_reward['name']} * {today_reward['cnt']}",end="\n\n")


def checkAlreadyLogged(dateFile):
    if os.path.exists(dateFile):
        with open(dateFile) as f:
            prevdate = f.read()
            if prevdate == dateToday:
                print("Already Logged In")
                showExitDialogue()
                sys.exit()
    return 1


def showExitDialogue():
    if getenv("ExitDialogue") == '1':
        input("Enter to exit...")


# def checkEnvFile(logDir):
#     envFile = os.path.join(logDir,".env")
#     if not os.path.exists(envFile):
#         shutil.copy(".env",os.path.join(logDir,".env"))           
#     else:
#         print("envfile already exists")


def getenv(var):
    return os.getenv(var)



def writeLog(filepath,data):
    with open(filepath,"w") as f:
        f.write(json.dumps(data,indent=4))

def sendDiscordMessage(message,reward,total_days,game):
    webhook = SyncWebhook.from_url(getenv("DiscordWebHookUrl"))
    embed = Embed(title=urls[game]['title'],color=urls[game]['color'],description=message)
    embed.add_field(name="Today's Reward",value=f"{reward['name']} * {reward['cnt']}",inline=True)
    embed.add_field(name="Total Checkins",value=total_days,inline=True)
    embed.set_thumbnail(url=reward['icon'])
    webhook.send(embed=embed,username=urls[game]['username'],avatar_url=urls[game]['icon'])




if __name__ == '__main__':
    username = getenv("USERNAME")
    logDir = fr"C:\Users\{username}\AppData\Local\hoyoAutoLogin"

    if not os.path.exists(logDir):
        print(f"creating {logDir}")
        os.mkdir(logDir)
        shutil.copy(".env",os.path.join(logDir,".env"))
    
    load_dotenv(dotenv_path=os.path.join(logDir,".env"))
    
    dateFile = os.path.join(logDir,"date.txt")
    dateToday = datetime.now().strftime("%D")

    
    # checkAlreadyLogged(dateFile)
    daily_login(['genshin','honkai'])

    try:
        # honkaiDaily() if getenv("HonkaiLogin") == '1' else ''
        # genshinDaily() if getenv("GenshinLogin") == '1' else ''
        # daily_login(['genshin','honkai'])
        dateToday = datetime.now().strftime("%D")
        if getenv("HonkaiLogin")=='1' or getenv("GenshinLogin")=='1':
            with open(dateFile,"w") as f:
                f.write(dateToday)
    except Exception as e:
        print(f"Error Occured: {e}")

    
    
    showExitDialogue()