from copy import deepcopy

from aiogram import Rounter
from aiogram.filters import Command, CommandStart, text
from aiogram.types import CallbackQuery, Message

from bot.database.test_database import user_dict_template, users_db
from bot.filters.custom_filter import IsDelBookmarkCallBackData, IsDigitCallbackData
from bot.keyboards.bookmarks import create_bookmarks_keyboard, create_edit_keyboard
from bot.keyboards.pagination import create_pagination_keybroad
from bot.lexicons.lexicon_en import Answer
from book.book_converter import book

Rounter: Rounter = Rounter()


@Rounter.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(Answer.start)
    user_id = message.from_user.id
    if user_id not in users_db:
        users_db[user_id] = deepcopy(user_dict_template)
        
@Rounter.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(Answer.help)
    
        
@Rounter.message(Command(commands='beginning'))
async def process_beginning_command(message: Message):
    user_id = message.from_user.id
    users_db[user_id]['page'] = 1
    text = book[users_db[user_id]['page']]
    await message.answer(
        text = text,
        reply_markup=create_pagination_keybroad(
            f'{users_db[users_db]["page"]}/{len(book)}'
        )
    )
@Rounter.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    user_id = message.from_user.id
    text = book[users_db[user_id]['page']]
    await message.answer(
        text = text,
        reply_markup=create_pagination_keybroad(
            f'{users_db[users_db]["page"]}/{len(book)}'
        )
    )
@Rounter.message(Command(commands='beginning'))
async def process_beginning_command(message: Message):
    user_id = message.from_user.id
    users_db[user_id]['page'] = 1
    text = book[users_db[user_id]['page']]
    await message.answer(
        text = text,
        reply_markup=create_pagination_keybroad(
            f'{users_db[user_id]["page"]}/{len(book)}'
        )
    )
@Rounter.message(Command(commands='bookmarks'))
async def process_bookmark_command(message: Message):
    user_id = message.from_user.id
    if users_db[user_id]['bookmark']:
        await message.answer(
            text = Answer.bookmarks,
            reply_markup=create_bookmark_keybroad(
                *users_db[user_id]["bookmark"]
            )
        )
    else:
        await message.answer(Answer.no_bookmark)
        
@Rounter.callback_query(Text(text='forward'))
async def process_forward_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    if users_db[user_id]['page'] < len(book):
        users_db[user_id]['page'] += 1
        text = book[users_db[user_id]['page']]
        await callback.message.edit_text(
            text = text,
            reply_markup=create_pagination_keybroad(
                f'{users_db[user_id]["page"]}/{len(book)}'
            )
        )
    await callback.answer()
@Rounter.callback_query(Text(text='backward'))
async def process_backward_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    if users_db[user_id]['page'] > len(book):
        users_db[user_id]['page'] -= 1
        text = book[users_db[user_id]['page']]
        await callback.message.edit_text(
            text = text,
            reply_markup=create_pagination_keybroad(
                f'{users_db[user_id]["page"]}/{len(book)}'
            )
        )
    await callback.answer()
    
@Rounter.callback_query(
    lambda x: '/' in x.data and x.data.replace('/', '').isdigit()
)
async def process_page_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    text = book[int(data)]
    await callback.answer('Page added to bookmark!!')
    
@Rounter.callback_query(IsDelBookmarkCallBackData)
async def process_del_backward_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    text = book[users_db[user_id]['page']]
    await callback.message.edit_text(
        text = text,
        reply_markup=create_pagination_keybroad(
            f'{users_db[user_id]["page"]}/{len(book)}'
        )
    )
    await callback.answer()
    
@Rounter.callback_query(Text(text='edit_bookmark'))
async def process_edit_backward_press(callback: CallbackQuery):
    await callback.message.answert(
        text = Answer.edit_bookwarks,
        reply_markup=create_pagination_keybroad(
            *users_db[callback.from_user.id]['bookmark']
        )
    )
    await callback.answer()
    
