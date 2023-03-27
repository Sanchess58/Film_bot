import json
import os
import random

import requests
import telebot
from dotenv import find_dotenv, load_dotenv

from get_inline_but import LIMIT, Typenumber, pages_number, pages_number_split

load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

i_run_once_has_been_run = False
ORIGINAL_NAME = "<b>Оригинальное название фильма:</b>"
RUSSIAN_NAME = "<b>Адаптированное название:</b>"
REALEASE_YEAR = "<b>Год премьеры:</b>"
RATING = "<b>Рейтинг:</b>"
DESC_NONE = "Описание фильма отсутсвует\U0001F61E \n"
TRAILER = "<b>Трейлер фильма🎬:</b>"
TRAILER_NONE = "Простите, трейлер и ссылка на фильм отсутствуют\U0001F61E"
LINK = "<b>Ссылка на фильм</b>🔗</a>"
TOKEN_KINO = os.getenv("KINO_TOKEN")
TOKEN_FILM = os.getenv("URL_FILM")


def request_name(search_name):
    url_name_film = (f"https://api.kinopoisk.dev/movie?&token={TOKEN_KINO}"
                     f"&search={search_name.text}&page=1&field=name"
                     "&selectFields=rating+id+type+enName+"
                     "year+alternativeName+description+poster"
                     "&limit=20&sortField[]=votes.kp&"
                     "sortField[]=premiere.world"
                     "&sortType[]=-1&sortType[]=-1")
    req = requests.get(url_name_film, params={})
    req_result = req.json()
    with open(f"all_films_{search_name.from_user.id}.json", "w") as js:
        json.dump(req_result, js, indent=2)
    f = open(f"all_films_{search_name.from_user.id}.json")
    data = json.load(f)
    random_film = random.choice(data['docs'])
    url_film = (f"https://apivb.info/api/videos.json?"
                f"id_kp={random_film['id']}&token={TOKEN_FILM}")
    req_film = requests.get(url_film, params={})
    req_result_film = req_film.json()
    with open(f"get_film_{search_name.from_user.id}.json", "w") as js:
        json.dump(req_result_film, js, indent=2)

    film_file = open(f"get_film_{search_name.from_user.id}.json")
    data_film_file = json.load(film_file)
    trailer = data_film_file[0]['trailer']
    replace_trailer = trailer.replace("embed/", "")
    good_url_trailer = replace_trailer.replace("www.youtube.com", "youtu.be")
    bot.send_message(search_name.chat.id,
                     (f"{ORIGINAL_NAME} {random_film['alternativeName']} \n"
                      f"{RUSSIAN_NAME} {data_film_file[0]['title_ru']} \n"
                      f"{REALEASE_YEAR} {random_film['year']} \n"
                      f"{RATING} {random_film['rating']['kp']} \n"
                      f"{random_film['description']}\n"
                      f"{TRAILER} {good_url_trailer} "
                      f"<a href='{random_film['poster']['previewUrl']}'>"
                      ".</a>\n"
                      f"<a href='{data_film_file[0]['iframe_url']}'>"
                      "<b>Ссылка на фильм</b>🔗</a> "),
                     parse_mode='html')
    bot.delete_message(search_name.chat.id, search_name.message_id)
    f.close()
    film_file.close()
    os.remove(f"get_film_{search_name.from_user.id}.json")
    os.remove(f"all_films_{search_name.from_user.id}.json")
    try:
        os.remove(f"buff_{search_name.from_user.id}.txt")
    except FileNotFoundError:
        pass


def requst(calld, year, genre, is_go):
    rand_pages = random.choice(pages_number)
    rand_pages_split = random.choice(pages_number_split)
    rand_typenumber = random.choice(Typenumber)
    global i_run_once_has_been_run
    if genre == "аниме":
        url_genres = (f"https://api.kinopoisk.dev/movie?search=4&"
                      f"search={genre}&search={year}&search=8-10&"
                      "search=!null&search=!null&field=typeNumber&"
                      "field=genres.name&field=year&field=rating.kp"
                      f"&field=name&field=votes.kp&limit={LIMIT}&"
                      f"page={rand_pages_split}&"
                      "sortField[]=premiere.world&sortField[]=votes.kp"
                      f"&sortType[]=1&sortType[]=1&token={TOKEN_KINO}")
        print(url_genres)

    elif genre == "мультфильм":
        url_genres = (f"https://api.kinopoisk.dev/movie?"
                      f"search={rand_typenumber}&search={genre}&"
                      f"search={year}&search=8-10&search=!null"
                      "&search=!null&field=typeNumber&"
                      "field=genres.name&field=year&"
                      "field=rating.kp&field=name&"
                      f"field=votes.kp&limit={LIMIT}&"
                      f"page={rand_pages_split}&"
                      f"sortField[]=premiere.world&sortField[]=votes.kp"
                      f"&sortType[]=1&sortType[]=1&token={TOKEN_KINO}")
    else:
        url_genres = (f"https://api.kinopoisk.dev/movie?search=1"
                      f"&search={genre}&search={year}&search=8-10&"
                      "search=!null&search=!null&field=typeNumber&"
                      f"field=genres.name&field=year&field=rating.kp&"
                      f"field=name&field=votes.kp&limit={LIMIT}&"
                      f"page={rand_pages_split}&"
                      "sortField[]=premiere.world&sortField[]=votes.kp&"
                      f"sortType[]=1&sortType[]=1&token={TOKEN_KINO}")
    url_year = (f"https://api.kinopoisk.dev/movie?&token={TOKEN_KINO}&"
                f"page={rand_pages}&limit={LIMIT}&field=rating.kp"
                f"&search=7.5-10&field=year&search={genre}&"
                "sortField[]=votes.kp&sortType[]=-1")
    if (is_go is False):
        req = requests.get(url_year, params={})
    elif (is_go is True or year == "2000-2022"):
        req = requests.get(url_genres, params={})
    req_result = req.json()

    with open(f"all_films_{calld.message.from_user.id}.json", "w") as js:
        json.dump(req_result, js, indent=2)

    f = open(f"all_films_{calld.message.from_user.id}.json")
    data = json.load(f)
    try:
        random_film = random.choice(data['docs'])
    except IndexError:
        bot.send_message(calld.message.chat.id,
                         "Повторите запрос еще раз")
        bot.register_next_step_handler(calld.message, )

    url_film = (f"https://apivb.info/api/videos.json"
                f"?id_kp={random_film['id']}&"
                f"token={TOKEN_FILM}")

    req_film = requests.get(url_film, params={})

    req_result_film = req_film.json()

    with open(f"get_film_{calld.message.from_user.id}.json", "w") as js:
        json.dump(req_result_film, js, indent=2)

    film_file = open(f"get_film_{calld.message.from_user.id}.json")

    data_file = json.load(film_file)

    try:
        trailer = data_file[0]['trailer']
        trailer_replac = trailer.replace("embed/", "")
        url_trailer = trailer_replac.replace("www.youtube.com", "youtu.be")
        if random_film['description'] is None:
            bot.send_message(calld.message.chat.id,
                             (f"{ORIGINAL_NAME} "
                              f"{random_film['alternativeName']} \n"
                              f"{RUSSIAN_NAME} {random_film['name']} \n"
                              f"{REALEASE_YEAR} {random_film['year']} \n"
                              f"{RATING} {random_film['rating']['kp']} \n"
                              f"{DESC_NONE}"
                              f"{TRAILER} {url_trailer} "
                              f"<a href='"
                              f"{random_film['poster']['previewUrl']}'"
                              ">.</a>\n"
                              f"<a href='{data_file[0]['iframe_url']}'>"
                              f"{LINK}"), parse_mode='html')

        if random_film['alternativeName'] is None:
            bot.send_message(calld.message.chat.id,
                             (f"{ORIGINAL_NAME} {random_film['name']} \n"
                              f"{REALEASE_YEAR} {random_film['year']} \n"
                              f"{RATING} {random_film['rating']['kp']}\n\n"
                              f"{random_film['description']}\n"
                              f"{TRAILER} {url_trailer} "
                              f"<a href= "
                              f"{random_film['poster']['previewUrl']}"
                              ">.</a>\n "
                              f"<a href='{data_file[0]['iframe_url']}'>"
                              f"{LINK}"), parse_mode='html')

        else:
            bot.send_message(calld.message.chat.id,
                             (f"{ORIGINAL_NAME} "
                              f"{random_film['alternativeName']} \n"
                              f"{RUSSIAN_NAME} {random_film['name']} \n"
                              f"{REALEASE_YEAR} {random_film['year']} \n"
                              f"{RATING} {random_film['rating']['kp']}\n\n"
                              f"{random_film['description']}\n"
                              f"{TRAILER} {url_trailer} "
                              f"<a href='"
                              f"{random_film['poster']['previewUrl']}'"
                              ">.</a>\n"
                              f"<a href='{data_file[0]['iframe_url']}'>"
                              f"{LINK}"), parse_mode='html')

    except IndexError:
        bot.send_message(calld.message.chat.id,
                         (f"{ORIGINAL_NAME} "
                          f"{random_film['alternativeName']} \n"
                          f"{RUSSIAN_NAME} {random_film['name']} \n"
                          f"{REALEASE_YEAR} {random_film['year']} \n"
                          f"{RATING} "
                          f"{random_film['rating']['kp']} \n\n"
                          f"{random_film['description']}\n"
                          f"<a href='{random_film['poster']['previewUrl']}"
                          "'>.</a>\n"
                          f"{TRAILER_NONE}"),
                         parse_mode='html')
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(calld.message.chat.id,
                         (f"{ORIGINAL_NAME} "
                          f"{random_film['alternativeName']} \n"
                          f"{RUSSIAN_NAME} {random_film['name']}\n"
                          f"{REALEASE_YEAR} {random_film['year']} \n"
                          f"{RATING} {random_film['rating']['kp']} \n\n"
                          f"{random_film['description']}\n"
                          f"{TRAILER} {url_trailer} "
                          f"{random_film['poster']['previewUrl']}\n"
                          f"Ссылка на фильм "
                          f"{data_file[0]['iframe_url']}🔗"))

    bot.answer_callback_query(callback_query_id=calld.id)
    bot.delete_message(calld.message.chat.id, calld.message.message_id)
    f.close()
    film_file.close()
    os.remove(f"get_film_{calld.message.from_user.id}.json")
    os.remove(f"all_films_{calld.message.from_user.id}.json")
    try:
        os.remove(f"buff_{calld.message.from_user.id}.txt")
    except FileNotFoundError:
        pass
