#secrets
try :
    from telegram_sec import telegram_token_harbor, telegram_token_web 
except :
    from tg_secrets.telegram_sec import (
        telegram_token_harbor, 
        telegram_token_web
        chatId1,
        chatId2,
        topic_back,
        topic_front,
        topic_other,
    )

from telegram import Update
from telegram.ext import (
    Application,
)

import asyncio



class telegramBotTools :
    def __init__(self):
        self.application_harbor = Application.builder().token(telegram_token_harbor).build()
        self.application_web = Application.builder().token(telegram_token_web).build()

    @classmethod
    async def sendMessageHarbor(cls, msg):
        self = telegramBotTools()
        await self.application_harbor.bot.send_message(
           chat_id=chatId1,
           text = msg,
           parse_mode='HTML',
        )

    @classmethod
    async def sendMessageWebback(cls, msg):
        self = telegramBotTools()
        await self.application_web.bot.send_message(
           chat_id=chatId2,
           message_thread_id=topic_back,
           text = msg,
           parse_mode='HTML',
        )

    @classmethod
    async def sendMessageWebfront(cls, msg):
        self = telegramBotTools()
        await self.application_web.bot.send_message(
           chat_id=chatId2,
           message_thread_id=topic_front,
           text = msg,
           parse_mode='HTML',
        )

    @classmethod
    async def sendMessageOther(cls, msg):
        self = telegramBotTools()
        await self.application_web.bot.send_message(
           chat_id=chatId2,
           message_thread_id=topic_other,
           text = msg,
           parse_mode='HTML',
        )


if __name__ == "__main__" :
    x = telegramBotTools()
    asyncio.run(x.sendMessage())