from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_mailout = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='all users', callback_data='all_users_pressed')
        ],
        [
            InlineKeyboardButton(text='admins', callback_data='admins_pressed')
        ],
        [
            InlineKeyboardButton(text='regular users', callback_data='regular_users_pressed')
        ]
        ]
)
