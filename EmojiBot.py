#Made by: Ignas Mikolaitis
#Website: ignuxas.com

import requests
from colored import fg
from time import sleep
from os import system

black = fg("#424242")
black2 = fg("#323232")
red = fg("#ff0000")
green = fg("#00ff00")
pinkred = fg("#E91E63")

def cls():
    system("cls")
def clt(StatusLen):
    StatLen = StatusLen
    print ("\033[A"+ " "*StatusLen + "\033[A")

cls()

#Settings

RefreshTime=input(black + "Time interval for every scan: " + green)

#Get Auth Token

authFile = open('DiscordKey.txt', 'r')
auth = authFile.readline()
authFile.close()

headers = {
    'authorization': auth
}

#Main function

links = []

with open('Links.txt') as f:
    for line in f:
        links.append(line.replace("\n", ""))

def Server(links):
    for link in links:
        url = "https://discord.com/api/v9/channels/"+link.split("/")[-1]+"/messages?limit=10"
        response = requests.request("GET", url, headers=headers).json()

        for message in response:
            if "reactions" in message:
                if(message["reactions"][0]["me"] == False):

                    #Reikia palaukt nes discord limituoja requestus

                    sleep(0.3)
                    r = requests.put("https://discord.com/api/v9/channels/"+link.split("/")[-1]+"/messages/"+message["id"]+"/reactions/"+str(message["reactions"][0]["emoji"]['name']+"/%40me"), headers=headers)
                    print(black+"ServerID: "+link.split("/")[-2] + " ("+link.replace(link.split("/")[-1], '')+")")
                    print(" ChannelID: "+link.split("/")[-1] + " ("+link+")")
                    print("  MessageID: "+message["id"])
                    if(r.status_code != 204):
                        print(red + "   Failed to send emoji {"+str(r.status_code)+"}\n")
                    else:
                        print(pinkred+"    Author: "+black+message["author"]["username"])
                        if "bot" in message:
                            print(pinkred+"     Bot: "+black+" True")
                        else:
                            print(pinkred+"     Bot:"+black+" False")
                        print(pinkred+"    @everyone: "+black+str(message["mention_everyone"]))
                        print(pinkred+"    Content: "+black+message["content"])
                        print(green + "   Sent Emoji {"+message["reactions"][0]["emoji"]['name']+"}\n")

while True:
    cls()
    Server(links)
    sleep(int(RefreshTime))