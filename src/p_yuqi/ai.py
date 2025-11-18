'''
neuro-writer with context & saving history
'''


import tracemalloc
from dotenv import load_dotenv
from os import getenv

from openai import AsyncOpenAI
from src.p_yuqi.core_and_writer import Writer


# create class neuro-writer
class Yuqi():

    def __init__(self):
        load_dotenv()
        API_KEY = getenv('OPENAI_API_KEY')
        self.client = AsyncOpenAI(api_key=API_KEY)
        self.user_context

    async def neuro_writer():
        