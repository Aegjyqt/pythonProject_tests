import contextlib
import os

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import BotBlocked, UserDeactivated, ChatNotFound
from dotenv import load_dotenv

import bot_db
import keyboards

load_dotenv()

bot = Bot(
    token=os.getenv('BOT_TOKEN'),
    parse_mode='HTML'
)

dp = Dispatcher(bot=bot, storage=MemoryStorage())


class MailoutPipeline(StatesGroup):
    mailout_init = State()
    mailout_all_users = State()
    mailout_regular_users = State()
    mailout_admins = State()


def admin(handler: callable):
    async def wrapper(message: types.Message):
        if message.from_user.id == 1405901798:
            return await handler(message)
        else:
            await message.answer('you\'re no admin!')

    return wrapper


@dp.message_handler(commands='start')
async def welcome_and_register(message: types.Message) -> None:
    db = bot_db.BotDb()
    db.add_to_database(user_id=message.from_user.id)
    await message.answer('welcome')


@dp.message_handler(commands='cancel', state='*')
async def exit_stage(message: types.Message, state: FSMContext) -> None:
    await message.reply(text='you\'ve cancelled')
    await state.finish()


@dp.message_handler(commands='mailout')
@admin
async def init_mailout(message: types.Message):
    await message.answer(text='Choose mailout type:', reply_markup=keyboards.kb_mailout)
    await MailoutPipeline.mailout_init.set()


@dp.callback_query_handler(text='all_users_pressed', state=MailoutPipeline.mailout_init)
async def ask_for_msg_to_all(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(text='Your message:')
    await state.set_state(MailoutPipeline.mailout_all_users)


@dp.message_handler(state=MailoutPipeline.mailout_all_users)
async def send_to_all_users(message: types.Message, state: FSMContext) -> None:
    db = bot_db.BotDb()
    for user_id in db.get_user_ids():
        with contextlib.suppress(BotBlocked, UserDeactivated, ChatNotFound):
            await message.send_copy(chat_id=user_id)
    await state.finish()


@dp.callback_query_handler(text='admins_pressed', state=MailoutPipeline.mailout_init)
async def ask_for_msg_to_admins(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(text='Your message:')
    await state.set_state(MailoutPipeline.mailout_admins)


@dp.message_handler(state=MailoutPipeline.mailout_admins)
async def send_to_all_admins(message: types.Message, state: FSMContext) -> None:
    db = bot_db.BotDb()
    for user_id in db.get_admin_ids():
        with contextlib.suppress(BotBlocked, UserDeactivated, ChatNotFound):
            await message.send_copy(chat_id=user_id)
    await state.finish()


@dp.callback_query_handler(text='regular_users_pressed', state=MailoutPipeline.mailout_init)
async def ask_for_msg_to_admins(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(text='Your message:')
    await state.set_state(MailoutPipeline.mailout_regular_users)


@dp.message_handler(state=MailoutPipeline.mailout_regular_users)
async def send_to_all_admins(message: types.Message, state: FSMContext) -> None:
    db = bot_db.BotDb()
    regular_users_ids_list = db.get_user_ids() - db.get_admin_ids()
    for user_id in regular_users_ids_list:
        with contextlib.suppress(BotBlocked, UserDeactivated, ChatNotFound):
            await message.forward(chat_id=user_id)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)


# TODO: при попытки пересылки сообщения переделать try с пустым except на suppress.
