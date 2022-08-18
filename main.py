from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import BotBlocked, UserDeactivated, ChatNotFound
from dotenv import load_dotenv
import os

import bot_databaseSQL

load_dotenv()

bot = Bot(
    token=os.getenv('BOT_TOKEN'),
    parse_mode='HTML'
)

dp = Dispatcher(bot=bot, storage=MemoryStorage())


class MailoutPipeline(StatesGroup):
    mailout_state = State()


def admin(handler: callable):
    async def wrapper(message: types.Message):
        if message.from_user.id == 1405901798:
            return await handler(message)
        else:
            await message.answer('you\'re no admin!')
    return wrapper


@dp.message_handler(commands='start')
async def welcome_and_register(message: types.Message) -> None:
    await bot_databaseSQL.add_to_database(user_id=message.from_user.id)
    await message.answer('welcome')


@dp.message_handler(commands='mailout')
@admin
async def init_mailout(message: types.Message):
    await message.answer(text='Your message for mailout:')
    await MailoutPipeline.mailout_state.set()


@dp.message_handler(state=MailoutPipeline.mailout_state)
async def send_hi_to_all(message: types.Message, state: FSMContext) -> None:
    for element in bot_databaseSQL.get_user_ids():
        try:
            await bot.forward_message(chat_id=element,
                                      from_chat_id=message.from_user.id,
                                      message_id=message.message_id)
        except (BotBlocked, UserDeactivated, ChatNotFound):
            pass
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
