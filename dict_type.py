from typing import Dict, List

from get_inline_but import INLINE_JANR, INLINE_SORTING, INLINE_YEAR

VOTE_JANR_YEAR = "Выберите с чего начать отбор фильма"
VOTE_JANR = "Выберите жанр"
VOTE_YEAR = "Выберите год выпуска"
voting_user: str = ("С чего хотите начать выбор фильма?\n "
                    "Напишите 'Год' выбор начнется с года \n "
                    "Напишите 'Жанр' выбор начнется с жанра")
dict_calldata: Dict[str, str] = {
        "triller": "триллер",
        "comedy": "комедия",
        "melodrama": "мелодрама",
        "cartoon": "мультфильм",
        "fantastic": "фэнтези",
        "family": "семейный",
        "anime": "аниме",
        "old_1980_1990": "1980-1990",
        "mid_1990_2000": "1991-2000",
        "mid_plus_2000_2010": "2001-2010",
        "new_2010_2022": "2011-2022",
}

vote: Dict[str, List[List[str]]] = {
        "Год выпуска \U0001F5D3": [INLINE_YEAR, VOTE_YEAR],
        "Жанр \U0001F4FD": [INLINE_JANR, VOTE_JANR],
        "Год выпуска и жанр": [INLINE_SORTING, VOTE_JANR_YEAR],
}
