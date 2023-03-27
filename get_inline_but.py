import os

import telebot
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
INLINE_YEAR = [["1980-1990", "old_1980_1990"],
               ["1991-2000", "mid_1990_2000"],
               ["2001-2010", "mid_plus_2000_2010"],
               ["2011-сейчас", "new_2010_2022"]]
INLINE_JANR = [[["Триллер", "triller"],
                ["Мелодрама", "melodrama"]],
               ["Комедия", "comedy"],
               ["Мультфильмы", "cartoon"],
               ["Фэнтези", "fantastic"],
               ["Аниме", "anime"],
               ["Семейный", "family"]]
INLINE_SORTING = [["Выбор года", "Year_first"],
                  ["Выбор жанра", "Genre_first"]]
LIMIT = 13
Typenumber = [3, 5]
pages_number = list(range(1, 100))
pages_number_split = list(range(1, 7))


def get_inline_button(inline_items, row_width=3):
    bot_types = telebot.types.InlineKeyboardButton
    inline_buttons = telebot.types.InlineKeyboardMarkup(row_width=row_width)

    for item in inline_items:
        if isinstance(item[0], list):
            one_line_buttons = []
            for i in item:
                one_line_buttons.append(bot_types(text=i[0],
                                                  callback_data=i[1]))
            inline_buttons.add(*one_line_buttons)
        else:
            inline_buttons.add(bot_types(text=item[0], callback_data=item[1]))
    return inline_buttons


def get_button(inline_button, word, message):
    key = get_inline_button(inline_button, 4)
    bot.send_message(message, word, reply_markup=key)
