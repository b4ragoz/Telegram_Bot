from aiogram import Dispatcher, Bot, types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import requests
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import urllib.request
import os
from aiogram.dispatcher.filters import Text
import time
from aiogram.dispatcher import FSMContext
import motor.motor_asyncio
from datetime import datetime
from aiogram.utils.exceptions import BotBlocked
from keyboards import stop_kb, menu_kb, sponsor_ikb
from other_data import channel1, channel2, channelID1, channelID2, tiktok_url, tiktok_headers, youtube_url, youtube_headers, instagram_url, instagram_headers, add_user
from private_data import TOKEN, client


bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


db = client['tg_bot']


class LinkHandler(StatesGroup):
    video_link = State()


@dp.message_handler(commands=['notify'])
async def notification(message: types.Message):
    if message.from_user.id == 1179022027:
        text = f'Привет, {message.from_user.full_name}! 🤖\n\nВ течение несольких часов я не работал, так как велись технические работы.\n\nСейчас я вновь запущен!\n\nС этого момента вся информация касательно моей работы будет выкладываться в моем официальном новостном канале 👇\n\n@autosaverinfo\n\nС любовью, ваш @autosavervids_bot ❤'
        users = await db.saverusers.find().to_list(None)
        for user in users:
            try:
                await bot.send_message(user['uid'], text, reply_markup=menu_kb)
            except Exception as err:
                pass


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    ikb = InlineKeyboardMarkup(row_width=1)
    ib1 = InlineKeyboardButton('Спонсор 1️⃣', url=channel1)
    ib2 = InlineKeyboardButton('Спонсор 2️⃣', url=channel2)
    ib3 = InlineKeyboardButton('Проверить подписку', callback_data='check')
    ikb.add(ib1, ib2, ib3)
    await bot.send_message(message.from_user.id, f'Приветствую, {message.from_user.full_name}! 👋\n\nЧтобы я начал свою работу тебе необходимо подписаться на наш информационный канал, чтобы всегда быть в курсе обновлений! 👇', reply_markup=ikb)
    user = await db.saverusers.find_one({"uid": message.from_user.id})
    if not user:
        await add_user(message.from_user.id, message.from_user.username)
    await message.delete()


@dp.message_handler(commands=['help'])
async def helper(message: types.Message):
    await bot.send_message(message.from_user.id, f'Привет, {message.from_user.full_name}, на связи техподдержка!🤖\n\nЕсли у тебя пояивились вопросы по моей работе, прежде чем писать модератору, прочитай данную статью 👇\nhttps://telegra.ph/Pravila-rabota-s-AutoSaver-12-06\n\nЕсли же вопрос не решился пиши\n@tastygrape')
    await message.delete()


@dp.message_handler(content_types=['text'], state=LinkHandler.video_link)
async def tiktok(message: types.Message, state: FSMContext):
    check1 = await bot.get_chat_member(chat_id=channelID1, user_id=message.from_user.id)
    check2 = await bot.get_chat_member(chat_id=channelID2, user_id=message.from_user.id)
    if (check2['status'] != 'left'):
        async with state.proxy() as data:
            data['video_link'] = message.text
            try:
                if 'tiktok' in data['video_link']:
                    await bot.send_message(message.from_user.id, 'Ожидайте, видео обрабатывается! 🤖')
                    querystring = {"link": (data['video_link'])}
                    response = requests.request("GET", tiktok_url, headers=tiktok_headers, params=querystring).json()
                    new_video = response['result']['aweme_detail']['video']['bit_rate'][0]['play_addr']['url_list'][0]
                    name = 'video.mp4'
                    urllib.request.urlretrieve(new_video, name)
                    await bot.send_video(message.from_user.id, open('video.mp4', 'rb'), caption='@autosavervids_bot')
                    await message.answer(f'Ваше видео готово ✅\n\nЖду следующую ссылку...\n\nПриостановить процесс 👇', reply_markup=stop_kb)
                    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'video.mp4')
                    os.remove(path)
                if 'youtube' in data['video_link']:
                    await bot.send_message(message.from_user.id, 'Ожидайте, видео обрабатывается! 🤖')
                    querystring = {"videoId": data['video_link'][27:38]}
                    response = requests.request("GET", youtube_url, headers=youtube_headers, params=querystring).json()
                    new_video = response['videos']['items'][1]['url']
                    name = 'video.mp4'
                    urllib.request.urlretrieve(new_video, name)
                    await bot.send_video(message.from_user.id, open('video.mp4', 'rb'), caption='@autosavervids_bot')
                    await message.answer(f'Ваше видео готово ✅\n\nЖду следующую ссылку...\n\nПриостановить процесс 👇',
                                         reply_markup=stop_kb)
                    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'video.mp4')
                    os.remove(path)
                if 'instagram' in data['video_link']:
                    await bot.send_message(message.from_user.id, 'Ожидайте, видео обрабатывается! 🤖')
                    querystring = {"url": data['video_link']}
                    response = requests.request("GET", instagram_url, headers=instagram_headers, params=querystring).json()
                    new_video = response['media']
                    name = 'video.mp4'
                    urllib.request.urlretrieve(new_video, name)
                    await bot.send_video(message.from_user.id, open('video.mp4', 'rb'), caption='@autosavervids_bot')
                    await message.answer(f'Ваше видео готово ✅\n\nЖду следующую ссылку...\n\nПриостановить процесс 👇',
                                         reply_markup=stop_kb)
                    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'video.mp4')
                    os.remove(path)
            except Exception as err:
                print(f'[{datetime.now()}]: {err}')
                await message.answer('Неверный формат ссылки. ❌\n\nПерепроверьте вводимые данные и повторите попытку.\nЕсли появились проблемы, остановите режим обработки и отправьте команду - /help', reply_markup=stop_kb)
    else:
        await message.answer('Похоже, что вы отписались от наших спонсоров. 😰\n\nПодпишитесь обратно и повторите попытку!', reply_markup=sponsor_ikb)


@dp.callback_query_handler(lambda c: c.data == 'stop', state=LinkHandler.video_link)
async def lauch(call: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    await state.reset_state()
    await bot.send_message(call.from_user.id, 'Я остановился! 🤖\n\nВ этом режиме я не читаю то, что ты мне отправляешь.\n\nТекущие площадки с которых я могу сохранить видео:\n- Tik Tok\n- Instagram Reels and Stories\n- YouTube Shorts\n\nЕсли нашел проблемы в моей работе, пропиши команду - /help', reply_markup=menu_kb)
    await call.message.delete()

@dp.callback_query_handler(lambda c: c.data == 'launch')
async def lauch(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    await LinkHandler.video_link.set()
    await bot.send_message(call.from_user.id, 'Я готов к обработке! 🤖\nОтправь мне ссылку на видео.')
    await call.message.delete()


@dp.callback_query_handler(lambda c: c.data == 'check')
async def checker(call: types.CallbackQuery):
    # await bot.answer_callback_query(call.id)
    user_channel_status = await bot.get_chat_member(chat_id=channelID1, user_id=call.from_user.id)
    user_channel_status2 = await bot.get_chat_member(chat_id=channelID2, user_id=call.from_user.id)
    if (user_channel_status2["status"] == 'member' and user_channel_status["status"] == 'member'):
        await bot.send_message(call.from_user.id, 'Поздравляю, теперь тебе доступно сохранение видеороликов без водной марки! 🎉\nСписок площадок с которых я могу сохранить видео:\n- Tik Tok\n- Instagram Reels and Stories\n- YouTube Shorts\n\nЧтобы скачать, жми на кнопку ниже! 👇', reply_markup=menu_kb)
        await call.message.delete()
    else:
        await bot.answer_callback_query(call.id, 'Ты не подписался на спонсоров!\nПодпишись и попробуй еще раз.', show_alert=True)


async def on_startup(_):
    print('online')


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)




