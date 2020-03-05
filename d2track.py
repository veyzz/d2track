import json
import os
import re
import requests
import time
from apihelper import *
from view import *


def main():
    with open('heroes.json', 'r') as file:
        HEROES = json.load(file)
    data = {}
    for p_id in get_players():
        name, link = get_profile(p_id)
        if name != "Undefined":
            heroes = get_heroes(p_id)
            total_games, total_wr = get_wl(p_id)
            last_heroes = get_heroes(p_id, 20)
            _, last_wr = get_wl(p_id, 20)
            data[p_id] = {
                "name": name,
                "link": link,
                "games": total_games,
                "winrate": total_wr,
                "heroes": heroes,
                "last_heroes": last_heroes,
                "last_winrate": last_wr
            }
        else:
            data[p_id] = {
                "name": name,
                "link": link,
                "games": 0,
                "winrate": 0,
                "heroes": [],
                "last_heroes": [],
                "last_winrate": 0
            }
    #to_console(data, HEROES)
    to_html(data, HEROES)
    os.system('google-chrome --new-window -app d2track.html')


def test():
    t = time.time()
    main()
    print("TOTAL TIME:", time.time() - t)


if __name__ == "__main__":
    test()
