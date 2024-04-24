import logging
import time
import asyncio
from datetime import datetime
import pytz
import multiprocessing as mp

from flask import Flask, request
from flask import Response, request

from tg_sender import telegramBotTools


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
bot = telegramBotTools()
#lock = mp.RLock()
app = Flask("webhook")


# harbor
@app.route('/hook', methods=['POST'])
async def metrics_handler():
    """ Handle a webhook post with basic HTTP authentication """
    postjson = request.json
    timedata = datetime.utcfromtimestamp(postjson['occur_at']).strftime('%Y-%m-%d %H:%M:%S')
    reply_text = f"<b>Time</b> : <code>{timedata}</code>\n"
    reply_text += f"<b>Type</b> : {postjson['type']}\n"
    reply_text += f"<b>Operator</b> : {postjson['operator']}\n"
    reply_text += f"<b>Namespace</b> : <code>{postjson['event_data']['repository']['namespace']}</code>\n"
    reply_text += f"<b>Repo Name</b> : <code>{postjson['event_data']['repository']['name']}</code>\n"
    reply_text += f"<b>Repo Type</b> : {postjson['event_data']['repository']['repo_type']}\n"
    reply_text += f"<b>Url</b> : {postjson['event_data']['resources'][0]['resource_url']}\n"
    reply_text += f"<b>Tag</b> : <code>{postjson['event_data']['resources'][0]['tag']}</code>\n"
    await bot.sendMessageHarbor(msg=reply_text)
    return Response(response='received harbor alerts',status=200,content_type='text/html;charset=utf-8')

# 後台告警
backmsgTemp = ""
@app.route('/webhook-back', methods=['POST'])
async def back_msg_handler():
    global backmsgTemp
    postjson = request.json
    dataKeys = postjson.keys()
    reply_text = ""
    timeNow = "📅 Received Time : <i>" + getNow() + "</i>\n"
    reply_text += timeNow
    for dataKey in dataKeys :
        reply_text += f"📍 <b>{dataKey}</b> : <code>{postjson[dataKey]}</code>\n"
    backmsgTemp += f"{reply_text}<i>================</i>\n"
    print(">>>>>後台<<<<<")
    print(backmsgTemp)
    await bot.sendMessageWebback(msg=reply_text)
    backmsgTemp = ""
    return Response(response='received backend alerts',status=200,content_type='text/html;charset=utf-8')
    # if len(backmsgTemp) + 300 >= 2600 :
    #     await bot.sendMessageWebback(msg=reply_text)
    #     # __stringFlusher(string=backmsgTemp)
    #     backmsgTemp = ""
    #     return Response(response='received backend alerts',status=200,content_type='text/html;charset=utf-8')
    # else :
    #     return Response(response='received backend alerts (temp)',status=200,content_type='text/html;charset=utf-8')

# 前台告警
frontmsgTemp = ""
@app.route('/webhook-front', methods=['POST'])
async def front_msg_handler():
    global frontmsgTemp
    postjson = request.json
    dataKeys = postjson.keys()
    reply_text = ""
    timeNow = "📅 Received Time : <i>" + getNow() + "</i>\n"
    reply_text += timeNow
    for dataKey in dataKeys :
        reply_text += f"📍 <b>{dataKey}</b> : <code>{postjson[dataKey]}</code>\n"
    frontmsgTemp += f"{reply_text}<i>================</i>\n"
    print(">>>>>前台<<<<<")
    print(frontmsgTemp)
    if len(frontmsgTemp) + 300 >= 2600 :
        await bot.sendMessageWebfront(msg=reply_text)
        # __stringFlusher(string=frontmsgTemp)
        frontmsgTemp = ""
        return Response(response='received frontend alerts',status=200,content_type='text/html;charset=utf-8')
    else :
        return Response(response='received frontend alerts (temp)',status=200,content_type='text/html;charset=utf-8')
    
# 其他告警
othermsgTemp = ""
@app.route('/webhook-other', methods=['POST'])
async def other_msg_handler():
    global othermsgTemp
    postjson = request.json
    dataKeys = postjson.keys()
    reply_text = ""
    timeNow = "📅 Received Time : <i>" + getNow() + "</i>\n"
    reply_text += timeNow
    for dataKey in dataKeys :
        reply_text += f"🥩 <b>{dataKey}</b> : <code>{postjson[dataKey]}</code>\n"
    othermsgTemp += f"{reply_text}<i>================</i>\n"
    print(">>>>>其他<<<<<")
    print(othermsgTemp)
    #if len(othermsgTemp) + 300 >= 2600 :
    await bot.sendMessageOther(msg=reply_text)
    # __stringFlusher(string=frontmsgTemp)
    othermsgTemp = ""
    return Response(response='received other alerts',status=200,content_type='text/html;charset=utf-8')
    #else :
    #    return Response(response='received other alerts (temp)',status=200,content_type='text/html;charset=utf-8')


@app.route('/health', methods=['GET'])
async def health_handler():
    await __checktimeback()
    await __checktimefront()
    #await __checktimeother()
    return Response(response='health check OK',status=200,content_type='text/html;charset=utf-8')

#def __stringFlusher(string:str):
#    string = ""

async def __checktimefront(): 
    global frontmsgTemp
    if frontmsgTemp != "" :
        await bot.sendMessageWebfront(msg=frontmsgTemp)
        #__stringFlusher(string=frontmsgTemp)
        frontmsgTemp = ""

async def __checktimeback(): 
    global backmsgTemp
    if backmsgTemp != "" :
        await bot.sendMessageWebback(msg=backmsgTemp)
        #__stringFlusher(string=backmsgTemp)
        backmsgTemp = ""

async def __checktimeother(): 
    global othermsgTemp
    if othermsgTemp != "" :
        await bot.sendMessageWebback(msg=othermsgTemp)
        #__stringFlusher(string=backmsgTemp)
        othermsgTemp = ""

def getNow():
    now = datetime.now(pytz.timezone('Asia/Taipei'))
    nowStr = f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}.{now.microsecond}"
    return nowStr

if __name__ == "__main__":
    pass