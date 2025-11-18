"""
neuro-writer with context & saving history
"""

import tracemalloc
from dotenv import load_dotenv
from os import getenv
from datetime import datetime, date

from openai import AsyncOpenAI
from core_and_writer import Writer

tracemalloc.start()


# create class neuro-writer
class Yuqi:

    def __init__(self):
        load_dotenv()
        API_KEY = getenv("OPENAI_API_KEY")
        self.client = AsyncOpenAI(api_key=API_KEY)
        self.user_context = {}
        self.limits = {}
        self.default_limit = 3
        self.last_reset = {}  

    # method request neuro-writer
    async def neuro_writer(self, user_id: int, text: str):
        await self._check_reset(user_id)

        if user_id not in self.limits:
            self.limits[user_id] = self.default_limit

        if user_id not in self.user_context:
            self.user_context[user_id] = ""

        writer = Writer(text, self.user_context, self.client)
        self.user_context[user_id] += "Клиент: " + text
        output = await writer.activate()
        self.user_context[user_id] += "Я: " + output

        return output

    # method clear history / use one request
    async def delete_history(self, user_id: int):
        await self._check_reset(user_id)

        if user_id not in self.limits:
            self.limits[user_id] = self.default_limit

        self.user_context[user_id] = ""
        self.limits[user_id] -= 1

        return self.limits[user_id]

    # internal method: check if need to reset daily limit
    async def _check_reset(self, user_id: int):
        today = date.today()
        if user_id not in self.last_reset or self.last_reset[user_id] < today:
            self.limits[user_id] = self.default_limit
            self.last_reset[user_id] = today
