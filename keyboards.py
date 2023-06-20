from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


menu_kb = InlineKeyboardMarkup(row_width=2)
m_b1 = InlineKeyboardButton('Запуск', callback_data='launch')
menu_kb.add(m_b1)


stop_kb = InlineKeyboardMarkup(row_width=1)
stop_b = InlineKeyboardButton('Остановить режим обработки', callback_data='stop')
stop_kb.add(stop_b)


sponsor_ikb = InlineKeyboardMarkup(row_width=1)
sponsor_b1 = InlineKeyboardButton('Спонсор 1️⃣', url=channel1)
sponsor_b2 = InlineKeyboardButton('Спонсор 2️⃣', url=channel2)
sponsor_ikb.add(sponsor_b1, sponsor_b2)
