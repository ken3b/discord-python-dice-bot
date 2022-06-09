import os
import re
import random
import string
import numpy
import hashlib
import discord
import time
from dotenv import load_dotenv

load_dotenv()
TOKEN = 'DiscordBotTokenHere'

client = discord.Client()

@client.event
async def on_ready():
        print('Active')

@client.event
async def on_message(message):
    if(message.content[0] == '!' and message.content[1] == 'r'): 
        mval = message.content
        x = re.split("[^0-9d+-/*//()]", mval[2:(len(mval)+1)])
        ctr = 0
        multiplicand = 1

        while(ctr<len(x)):
            if(x[ctr] == ""):
                x.pop(ctr)
            else:
                ctr+=1

        print(x)

        ctr = 0

        for i in x:
            valall = [x[ctr].find("+"), x[ctr].find("-"), x[ctr].find("*"), x[ctr].find("/"), x[ctr].find("("), x[ctr].find(")")]
            for j in range(len(valall)):
                if(valall[j] == -1):
                    valall[j] = 100000
            if(min(valall) < 100):
                if(valall[0] != -1 and len(x[ctr]) > 1 and min(valall) == valall[0]):
                    if(i.find("+") > 0):
                        x.insert(ctr, x[ctr][0:(x[ctr].find("+"))])
                        x.insert(ctr + 1, "+")
                        x[ctr+2] = x[ctr+2][(x[ctr+2].find("+")+1):len(x[ctr+2])]
                    else:
                        x.insert(ctr, "+")
                        x[ctr+1] = x[ctr+1][(x[ctr+1].find("+")+1):len(x[ctr+1])]
                elif(valall[1] != -1 and len(x[ctr]) > 1 and min(valall) == valall[1]):
                    if(i.find("-") > 0):
                        x.insert(ctr, x[ctr][0:(x[ctr].find("-"))])
                        x.insert(ctr + 1, "-")
                        x[ctr+2] = x[ctr+2][(x[ctr+2].find("-")+1):len(x[ctr+2])]
                    else:
                        x.insert(ctr, "-")
                        x[ctr+1] = x[ctr+1][(x[ctr+1].find("-")+1):len(x[ctr+1])]
                elif(valall[2] != -1 and len(x[ctr]) > 1 and min(valall) == valall[2]):
                    if(i.find("*") > 0):
                        x.insert(ctr, x[ctr][0:(x[ctr].find("*"))])
                        x.insert(ctr + 1, "*")
                        x[ctr+2] = x[ctr+2][(x[ctr+2].find("*")+1):len(x[ctr+2])]
                    else:
                        x.insert(ctr, "*")
                        x[ctr+1] = x[ctr+1][(x[ctr+1].find("*")+1):len(x[ctr+1])]
                elif(valall[3] != -1 and len(x[ctr]) > 1 and min(valall) == valall[3]):
                    if(i.find("/") > 0):
                        x.insert(ctr, x[ctr][0:(x[ctr].find("/"))])
                        x.insert(ctr + 1, "/")
                        x[ctr+2] = x[ctr+2][(x[ctr+2].find("/")+1):len(x[ctr+2])]
                    else:
                        x.insert(ctr, "/")
                        x[ctr+1] = x[ctr+1][(x[ctr+1].find("/")+1):len(x[ctr+1])]
                elif(valall[4] != -1 and len(x[ctr]) > 1 and min(valall) == valall[4]):
                    if(i.find("(") > 0):
                        x.insert(ctr, x[ctr][0:(x[ctr].find("("))])
                        x.insert(ctr + 1, "+")
                        x[ctr+2] = x[ctr+2][(x[ctr+2].find("(")+1):len(x[ctr+2])]
                    else:
                        x.insert(ctr, "(")
                        x[ctr+1] = x[ctr+1][(x[ctr+1].find("(")+1):len(x[ctr+1])]
                elif(valall[5] != -1 and len(x[ctr]) > 1 and min(valall) == valall[5]):
                    if(i.find(")") > 0):
                        x.insert(ctr, x[ctr][0:(x[ctr].find(")"))])
                        x.insert(ctr + 1, ")")
                        x[ctr+2] = x[ctr+2][(x[ctr+2].find(")")+1):len(x[ctr+2])]
                    else:
                        x.insert(ctr, ")")
                        x[ctr+1] = x[ctr+1][(x[ctr+1].find(")")+1):len(x[ctr+1])]
            ctr+=1

        ctr = 0
        answer = ""
        Fin = run(x,message.author.name)
        if(Fin[0].find("Error:") >= 0):
            answer = Fin[0]
        elif(len(Fin[0]) > (1986-len(str(Fin[1])))):
            answer = "total: " + str(Fin[1])
        else: 
            answer = "roll: " + Fin[0]+ " total: " + str(Fin[1])
        await message.channel.send(answer)


def run(x, y):
    seedVal = int(str(int(time.time()*1000000)) + str(hashlib.sha512(y.encode()))[33:-1],16)
    multiplicand = 1
    ctr = 0
    tally = 0
    out = ""
    while (ctr < len(x)):
        i = x[ctr]
        if(i == "("): 
            subCtr = 0
            parenLevel = 1
            roll = 0
            for i in x[ctr+1:len(x)+1]:
                if(i == ")" and parenLevel == 1):
                    temp = x[ctr+1:subCtr+ctr+1]
                    RetVal = run(temp, y)
                    if(RetVal[0].find("Error:") >= 0):
                        return RetVal
                    if(len(out) < 2500):
                        out += RetVal[0]
                    roll = RetVal[1]
                elif(i == "("):
                    parenLevel += 1
                elif(i == ")"):
                    parenLevel -= 1
                subCtr+=1
                if((subCtr+ctr) == (len(x)-1)):
                    out = "Error: Missing Parenthesis."
                    return (out,tally)
            
            x = x[0:ctr]+x[ctr+subCtr+2:len(x)+1]
            x.insert(ctr+1,str(roll))
            ctr -= 1

        elif (i.find("d") != -1):
            print(i)
            if(len(out) < 2500):
                out += str(i) + ": "
            if(len(i[0:i.find("d")]) > 0):
                diceCnt = int(i[0:i.find("d")])
            else:
                diceCnt = 1
            diceVal = int(i[(i.find("d")+1):(len(i)+1)])
            roll = 0
            print("[",end="")
            for i in range(diceCnt):
                userSeed = random.Random(seedVal)
                temp = userSeed.randint(1,diceVal)
                if(i == diceCnt-1):
                    print(f"{temp}", end="")
                    if(len(out) < 2500):
                        out += str(temp) + " "
                else:
                    print(f"{temp}, ", end="")
                    if(len(out) < 2500):
                        out += str(temp) + ", "
                roll += temp
                seedVal += 1
            print(f"] roll: {roll}")

            if((len(x) > ctr+1 and x[ctr+1] == "*") or (len(x) > ctr+1 and x[ctr+1] == "/")):
                multiplicand = roll
                print(tally)
                print(roll)
            elif(ctr == 0):
                tally = roll
            else:
                if(x[ctr-1] == "+"):
                    tally += roll
                elif(x[ctr-1] == "-"):
                    tally -= roll
                elif(x[ctr-1] == "*"):
                    tally += multiplicand * roll
                    multiplicand = 1
                elif(x[ctr-1] == "/"):
                    tally += multiplicand / roll
                    multiplicand = 1
            if(ctr < len(x)-1 and x[ctr+1].isdigit()):
                out = "Error: Missing Operator."
                tally = 0
                return (out,tally)
                
        elif (i.isdigit()):
            if(len(x) > ctr+1 and (x[ctr+1] == "*" or x[ctr+1] == "/")):
                multiplicand *= int(i)
            elif(ctr == 0):
                tally = int(i)
            else:
                if(x[ctr-1] == "+"):
                    tally += int(i)
                elif(x[ctr-1] == "-"):
                    tally -= int(i)
                elif(x[ctr-1] == "*"):
                    tally += multiplicand * int(i)
                    multiplicand = 1
                else:
                    tally += multiplicand / int(i)
                    multiplicand = 1
            if(ctr < len(x) and (x[ctr+1].isdigit() or x[ctr+1].find("d") != -1)):
                out = "Error: Missing Operator."
                tally = 0
                return (out,tally)
        
        ctr+=1

    return (out, tally)


client.run(TOKEN)
