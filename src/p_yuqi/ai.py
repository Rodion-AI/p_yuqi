"""
neuro-writer with context & saving history
"""

import tracemalloc
from dotenv import load_dotenv
from os import getenv

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
        if user_id not in self.limits:
            self.limits[user_id] = self.default_limit

        if user_id not in self.user_context:
            self.user_context[user_id] = ""

        writer = Writer(text, self.user_context, self.client)
        self.user_context[user_id] += "Клиент: " + text
        output = await writer.activate()
        self.user_context[user_id] += "Я: " + output

        return output
    
    # method clear history
    async def delete_history(self, user_id: int):
        if user_id not in self.limits:
            self.limits[user_id] = self.default_limit

        self.user_context[user_id] = ""

        self.limits[user_id] -= 1

        return self.limits[user_id]
