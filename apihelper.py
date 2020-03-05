import json
import os
import re
import requests


def get_heroes_list():
    """ Gets ALL heroes.
    Writes it to the file.

    """
    data = requests.get("https://api.opendota.com/api/heroes").json()
    heroes = {}
    for obj in data:
        heroes[obj["id"]] = {
            "dota_name": re.search("npc_dota_hero_(.*)", obj["name"]).group(1),
            "name": obj["localized_name"]
        }
    with open('heroes.json', 'w') as file:
        json.dump(heroes, file, indent=4)


def get_players():
    """ Gets players from server log file
    :return: List of 10 numbers (ID).

    """
    path = f'/home/{os.getlogin()}/.steam/steam/steamapps/common/dota 2 beta/game/dota/server_log.txt'
    with open(path, 'r') as file:
        string = file.read()
    return list(map(int, re.findall('U:1:(\d+)', \
        re.findall('DOTA_GAMEMODE_CM|DOTA_GAMEMODE_ALL_DRAFT (.*)', string)[-1])))[:10:]


def get_heroes(player_id, limit=0, min_games=3):
    """ Gets the heroes the player has played the most.
    :param player_id: Player's ID (number).
    :param limit: Number of matches to limit to.
    :param min_games: Optional. Min number of games played on the hero.
    :return: List with up to 3 dict objects.

    """
    url = f"https://api.opendota.com/api/players/{player_id}/heroes"
    payload = {"limit": limit, "having": min_games}
    response = requests.get(url, params=payload)
    if response.status_code != 200:
        raise Exception("Connection fault", response.status_code,
                        response.reason)
    data = [{
        key: value
        for key, value in obj.items()
        if key in ("hero_id", "last_played", "games", "win")
    } for obj in response.json()[0:3]]
    return data


def get_wl(player_id, limit=0):
    """ Gets amount of games played and winrate.
    :param player_id: Player's ID (number).
    :param limit: Number of matches to limit to.
    :return: Turple with 2 values amount, winrate.

    """
    url = f"https://api.opendota.com/api/players/{player_id}/wl"
    payload = {"limit": limit}
    response = requests.get(url, params=payload)
    if response.status_code != 200:
        raise Exception("Connection fault", response.status_code,
                        response.reason)
    data = response.json()
    amount = data['win'] + data['lose']
    if not amount:
        return (0, 0)
    result = (data['win'] + data['lose'],
              f"{round(100*data['win']/(data['win']+data['lose']), 2)}%")
    return result


def get_profile(player_id):
    """ Gets user profile name and link.
    :param player_id: Player's ID (number).
    :return: Turple with name, link.

    """
    url = f"https://api.opendota.com/api/players/{player_id}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Connection fault", response.status_code,
                        response.reason)
    data = response.json()
    try:
        name = data["profile"]["personaname"]
    except KeyError:
        name = "Undefined"
    link = f"https://www.dotabuff.com/players/{player_id}"
    return name, link
