import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.types import KeyboardButton as KB
from ai import Yuqi

load_dotenv()
yuqi = Yuqi()

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await yuqi.delete_history(message.from_user.id)  # type: ignore
    await message.answer(
        "Приветствую! Меня зовут Юйци и я писатель художественной литературы. Нажмите /help, чтобы больше узнать про мои способности."
    )


@dp.message(Command("help"))
async def command_help_handler(message: Message):
    """
    This handler receives messages with `/help` command
    """

    def reply_keyboard():
        buttons = [[KB(text="Новый запрос")]]
        return ReplyKeyboardMarkup(
            keyboard=buttons,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder=("Пожалуйста, нажмите кнопку ниже"),
        )

    async def send_message_keyboard(message: Message, text: str, markup):
        await message.answer(text, reply_markup=markup)

    await send_message_keyboard(
        message,
        "Я отлично умею стилизовать или писать тексты в художественном стиле. Ниже вы можете найти кнопку для нового запроса.",
        reply_keyboard(),
    )


@dp.message(F.text == "Новый запрос")
async def new_request(message: Message):
    await yuqi.delete_history(message.from_user.id)  # type: ignore
    await message.answer("Переходим к другому тексту")


@dp.message()
async def echo_handler(message: Message):
    """
    Handles any incoming text message.
    """
    if not message.text:
        await message.answer("Я работаю только с текстом, любимый автор.")
        return

    try:
        response = await yuqi.neuro_writer(
            user_id=message.from_user.id, text=message.text  # type: ignore
        )
        await message.answer(response)

    except TypeError:
        await message.answer("Не могу обработать такое сообщение.")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
