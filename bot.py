from config import bot, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.utils.exceptions import ChatNotFound

import schedule
import asyncio

from aiogram.types import PreCheckoutQuery, SuccessfulPayment

import re

from database_handler import database_handler
from menu_handler     import menu_handler

dh = database_handler()
mh = menu_handler()

email_pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
phone_pattern = r"^(?:\+375|8-?375|375)?[1-9]\d{8}$|^(?:\+7|8-?7|7)?[1-9]\d{9}$"

class UserState(StatesGroup):
    NAME          = State()
    EMAIL         = State()
    PHONE         = State()
    MENU          = State()
    ANSWER        = State()
    PAY           = State()
    ADMIN         = State()
    PHOTO         = State()
    VIDEO         = State()
    VOICE         = State()
    CONFIRM_PHOTO = State()
    CONFIRM_VOICE = State()
    CONFIRM_VIDEO = State()
    CONFIRM_TEXT  = State()
    MESSAGE       = State()

button_handlers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]

@dp.message_handler(Command('start'))
async def start(message: types.Message):
    try:
        dh.include_id(str(message.from_user.id))
        await bot.send_message(message.from_user.id, "Как вас зовут?")
        await UserState.NAME.set()
    except Exception as e:
        print("ERROR: ", e)

@dp.message_handler(Command('admin'))
async def admin(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "С возвращением!", reply_markup=mh.admin_menu)
        await UserState.ADMIN.set()
    except Exception as e:
        print("ERROR: ", e)

@dp.message_handler(text="Добавить фото", state=UserState.ADMIN)
async def add_photo(message: types.Message):
    await bot.send_message(message.from_user.id, "Фотогафия будет появляться в боте автоматически каждый день.\nПришлите фотографию.")
    await UserState.PHOTO.set()

@dp.message_handler(text="Добавить видео", state=UserState.ADMIN)
async def add_video(message: types.Message):
    await bot.send_message(message.from_user.id, "Видео будет появляться в боте автоматически каждый день.\nПришлите видео.")
    await UserState.VIDEO.set()

@dp.message_handler(text="Добавить голосовое сообщение", state=UserState.ADMIN)
async def add_voice(message: types.Message):
    await bot.send_message(message.from_user.id, "Голосовое сообщение будет появляться в боте автоматически каждый день.\nЗапишите голосовое сообщение.")
    await UserState.VOICE.set()

@dp.message_handler(text="Добавить текстовое сообщение", state=UserState.ADMIN)
async def add_voice(message: types.Message):
    await bot.send_message(message.from_user.id,"Текстовое сообщение будет появляться в боте автоматически каждый день.\nЗапишите сообщение.")
    await UserState.MESSAGE.set()

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=UserState.MESSAGE)
async def choose_text(message: types.Message, state: FSMContext):
    try:
        text = message.text
        await bot.send_message(message.from_user.id, f"Вы выбрали это текстовое сообщение:\n\n{text}\n\nХотите добавить его?", reply_markup=mh.choose)
        await state.update_data(chosen_text=text)
        await UserState.CONFIRM_TEXT.set()
    except Exception as e:
        print(e)

@dp.message_handler(text="да", state=UserState.CONFIRM_TEXT)
async def confirm_text(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        chosen_text = data.get("chosen_text")
        dh.set_admin_message(chosen_text)
        await bot.send_message(message.from_user.id, "Спасибо за текстовое сообщение", reply_markup=mh.admin_menu)
        await UserState.ADMIN.set()
    except Exception as e:
        print(e)

@dp.message_handler(text="нет", state=UserState.CONFIRM_TEXT)
async def cancel_text(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Отменено. Введите другой текст или отмените операцию.", reply_markup=mh.admin_menu)
    await UserState.ADMIN.set()

@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=UserState.PHOTO)
async def choose_photo(message: types.Message, state: FSMContext):
    try:
        photo = message.photo[-1]
        await bot.send_photo(message.from_user.id, photo.file_id, "Вы выбрали это изображение. Хотите загрузить его?", reply_markup=mh.choose)
        await state.update_data(chosen_photo=photo.file_id)
        await UserState.CONFIRM_PHOTO.set()
    except Exception as e:
        print(e)

@dp.message_handler(text="да", state=UserState.CONFIRM_PHOTO)
async def confirm_photo(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        photo_file_id = data.get("chosen_photo")
        dh.set_admin_photo(photo_file_id)
        await bot.send_message(message.from_user.id, "Спасибо за фотографию", reply_markup=mh.admin_menu)
        await UserState.ADMIN.set()
    except Exception as e:
        print(e)

@dp.message_handler(text="нет", state=UserState.CONFIRM_PHOTO)
async def cancel_photo(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Отменено. Выберите другое изображение или отмените операцию.", reply_markup=mh.admin_menu)
    await UserState.ADMIN.set()

@dp.message_handler(content_types=types.ContentTypes.VOICE, state=UserState.VOICE)
async def choose_voice(message: types.Message, state: FSMContext):
    try:
        voice = message.voice
        await bot.send_voice(message.from_user.id, voice.file_id, "Вы выбрали это голосовое сообщение. Хотите загрузить его?", reply_markup=mh.choose)
        await state.update_data(chosen_voice=voice.file_id)
        await UserState.CONFIRM_VOICE.set()
    except Exception as e:
        print(e)

@dp.message_handler(text="да", state=UserState.CONFIRM_VOICE)
async def confirm_voice(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        voice_file_id = data.get("chosen_voice")
        dh.set_admin_voice(voice_file_id)
        await bot.send_message(message.from_user.id, "Спасибо за голосовое сообщение", reply_markup=mh.admin_menu)
        await UserState.ADMIN.set()
    except Exception as e:
        print(e)

@dp.message_handler(text="нет", state=UserState.CONFIRM_VOICE)
async def cancel_voice(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Отменено. Выберите другое голосовое сообщение или отмените операцию.", reply_markup=mh.admin_menu)
    await UserState.ADMIN.set()

@dp.message_handler(content_types=types.ContentTypes.VIDEO, state=UserState.VIDEO)
async def choose_video(message: types.Message, state: FSMContext):
    try:
        video = message.video
        await bot.send_video(message.from_user.id, video.file_id, caption="Вы выбрали это видео. Хотите загрузить его?", reply_markup=mh.choose)
        await state.update_data(chosen_video=video.file_id)
        await UserState.CONFIRM_VIDEO.set()
    except Exception as e:
        print(e)

@dp.message_handler(text="да", state=UserState.CONFIRM_VIDEO)
async def confirm_video(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        video_file_id = data.get("chosen_video")
        dh.set_admin_video(video_file_id)
        await bot.send_message(message.from_user.id, "Спасибо за видео", reply_markup=mh.admin_menu)
        await UserState.ADMIN.set()
    except Exception as e:
        print(e)

@dp.message_handler(text="нет", state=UserState.CONFIRM_VIDEO)
async def cancel_video(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Отменено. Выберите другое видео или отмените операцию.", reply_markup=mh.admin_menu)
    await UserState.ADMIN.set()

@dp.message_handler(text="Выйти", state=UserState.ADMIN)
async def back(message: types.Message):
    await bot.send_message(message.from_user.id, "выберете интересующую тему", reply_markup=mh.menu)
    await UserState.ANSWER.set()

@dp.message_handler(Command('callall'))
async def callall(message: types.Message):
    answer = dh.get_admin_content()
    idies = dh.get_all_id()
    if answer[0] is not None:
        for item in answer:
            for user_id in idies:
                try:
                    if item['type'] == 1 and item['id'] is not None:
                        await bot.send_photo(user_id, item['id'])
                    elif item['type'] == 2 and item['id'] is not None:
                        await bot.send_video(user_id, item['id'])
                    elif item['type'] == 3 and item['id'] is not None:
                        await bot.send_voice(user_id, item['id'])
                    elif item['type'] == 4 and item['id'] is not None:
                        await bot.send_message(user_id, item['id'])
                except ChatNotFound:
                    print(f"ChatNotFound: Невозможно отправить сообщение пользователю с ID {user_id}")

@dp.message_handler(state=UserState.NAME)
async def choose_name(message: types.Message):
    try:
        if dh.include_name(message.from_user.id, message.text) is False:
            await UserState.EMAIL.set()
            await bot.send_message(message.from_user.id, "Укажите свой email")
        else:
            await UserState.EMAIL.set()
            await bot.send_message(message.from_user.id, "У вас уже введено имя, введите email")
    except Exception as e:
        print("ERROR: ", e)

@dp.message_handler(state=UserState.EMAIL)
async def choose_email(message: types.Message):
    try:
        if re.match(email_pattern, message.text) is not None:
            if dh.include_email(message.from_user.id, message.text) is False:
                await UserState.PHONE.set()
                await bot.send_message(message.from_user.id, "Укажите свой телефон")
            else:
                await UserState.PHONE.set()
                await bot.send_message(message.from_user.id, "У вас уже есть email, введите номер телефона") 
        else:
            await UserState.EMAIL.set()
            await bot.send_message(message.from_user.id, "Укажите корректный email") 
    except Exception as e:
        print("ERROR: ", e) 

@dp.message_handler(state=UserState.PHONE)
async def choose_phone(message: types.Message):
    try:
        if re.match(phone_pattern, message.text):
            if dh.include_phone(message.from_user.id, message.text) is False:
                await UserState.MENU.set()
                await bot.send_message(message.from_user.id, "выберете интересующую тему", reply_markup=mh.menu)
            else:
                await UserState.MENU.set()
                await bot.send_message(message.from_user.id, "выберете интересующую тему", reply_markup=mh.menu)
        else:
            await UserState.PHONE.set()
            await bot.send_message(message.from_user.id, "Укажите корректный телефон")  
    except Exception as e:
        print("ERROR: ", e)

@dp.callback_query_handler(text_contains='qq_', state=UserState.MENU)
async def choose_question(call: types.CallbackQuery, state: FSMContext):
    try:
        button_text = call.data[3:]
        if button_text in button_handlers:
            global theme
            theme = button_text
            await UserState.ANSWER.set()
            await bot.send_message(call.from_user.id, f"Введите свой вопрос по этой теме", reply_markup=mh.menu_button)
            await call.answer()  # Сброс состояния кнопки
    except Exception as e:
        print(e)

@dp.message_handler(text="меню", state=UserState.ANSWER)
async def return_menu(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(message.from_user.id, "Выберите интересующую тему", reply_markup=mh.menu)
        await state.reset_state()
    except Exception as e:
        print(e)

@dp.message_handler(text="Отправить запрос на оплату", state=UserState.ANSWER)
async def pay(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(message.from_user.id, "Вы отправили заявку", reply_markup=mh.menu_button)
        dh.add_pay(message.from_user.id)
        await state.reset_state()
    except Exception as e:
        print(e)

@dp.message_handler(state=UserState.ANSWER)
async def handle_answer(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(message.from_user.id, "Введите свой вопрос по выбранной теме", reply_markup=mh.menu_button)
        dh.add_answer(message.from_user.id, message.text, theme)
        await state.reset_state()
    except Exception as e:
        print(e)

executor.start_polling(dp, skip_updates=True)