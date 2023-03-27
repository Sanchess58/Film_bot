import json
import os
from dotenv import load_dotenv, find_dotenv
import telebot
from telebot import types

from dict_type import dict_calldata, vote
from get_inline_but import (INLINE_JANR, INLINE_YEAR, get_button,
                            get_inline_button)
from requst import request_name, requst

load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
genre = ""
year = ""
is_genre_and_year = False
INPUT_NAME_FILM = ("Введите название фильма"
                   "(название фильма вводите соответственно "
                   "названию российской адаптации)")
WARNING_MESSAGE = "Не понимаю, что ты пишешь, нажми еще раз кнопки"
GREETING = "Здравствуйте, варианты выбора фильмов"


@bot.message_handler(commands=['start'])
def button_message(message):

    with open('json_files/users.json', "r") as file:
        user_count = json.load(file)

    if str(message.from_user.username) not in user_count:

        user_count[message.from_user.username] = {}

        with open('json_files/users.json', "w") as file:
            json.dump(user_count, file, indent=4)

    key_mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
    year = types.KeyboardButton("Год выпуска \U0001F5D3")
    genre = types.KeyboardButton("Жанр \U0001F4FD")
    year_and_genre = types.KeyboardButton("Год выпуска и жанр")
    name_film = types.KeyboardButton("Название фильма")
    key_mark.add(year, genre, year_and_genre, name_film)
    bot.send_message(message.chat.id, GREETING, reply_markup=key_mark)


@bot.message_handler(content_types='text')
def create_janr(message):
    try:
        if message.text == "Название фильма":
            bot.send_message(message.chat.id, INPUT_NAME_FILM)
            bot.register_next_step_handler(message, check_name_film)
        else:
            year_and_genre.has_been_called = False
            key = get_inline_button(vote.get(message.text)[0], 4)
            bot.send_message(message.chat.id,
                             vote.get(message.text)[1],
                             reply_markup=key)
    except TypeError:
        bot.send_message(message.chat.id, WARNING_MESSAGE)


def check_name_film(message):
    request_name(message)


@bot.callback_query_handler(func=lambda call:
                            call.data.startswith('Year_first')
                            or call.data.startswith('Genre_first'))
def year_and_genre(back_r):
    global i_run_once_has_been_run
    year_and_genre.has_been_called = True
    i_run_once_has_been_run = False
    if (back_r.data == "Year_first" or
            back_r.data == "triller" or
            back_r.data == "comedy" or
            back_r.data == "melodrama" or
            back_r.data == "cartoon" or
            back_r.data == "fantastic" or
            back_r.data == "family" or
            back_r.data == "anime"):
        get_button(INLINE_YEAR, "Выберите год", back_r.message.chat.id)
    if (back_r.data == "Genre_first" or
            back_r.data == "old_1980_1990" or
            back_r.data == "mid_1990_2000" or
            back_r.data == "mid_plus_2000_2010" or
            back_r.data == "new_2010_2022"):
        get_button(INLINE_JANR, "Выберите жанр", back_r.message.chat.id)
    bot.answer_callback_query(callback_query_id=back_r.id)
    bot.delete_message(back_r.message.chat.id, back_r.message.message_id)


@bot.callback_query_handler(func=lambda call:
                            not call.data.startswith('Year_first')
                            or not call.data.startswith('Genre_first'))
def check_film(back_r):
    global i_run_once_has_been_run, is_genre_and_year, genre, year
    if year_and_genre.has_been_called:
        with open(f"buff_{back_r.message.from_user.id}.txt", "w",
                  encoding='utf-8') as file:
            file.write(f"{dict_calldata.get(back_r.data)}")
        file = open(f"buff_{back_r.message.from_user.id}.txt",
                    encoding="utf-8")
        check = file.read()
        if check[:1] == "1" or check[:1] == "2":
            year = check
        else:
            genre = check
        if i_run_once_has_been_run is False:
            year_and_genre(back_r)
            i_run_once_has_been_run = True

        file.close()
        if year != "" and genre != "":
            is_genre_and_year = True
            requst(back_r, year, genre, is_genre_and_year)
            genre = ""
            year = ""
    else:
        if (dict_calldata.get(back_r.data)[:1] == "1" or
                dict_calldata.get(back_r.data)[:1] == "2"):
            is_genre_and_year = False
        else:
            is_genre_and_year = True
        print(is_genre_and_year)
        requst(back_r, "2000-2022",
               dict_calldata.get(back_r.data), is_genre_and_year)


bot.infinity_polling()
