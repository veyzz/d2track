#TODO: GUI
import requests
import re
import json
import os
import time


with open('heroes.json', 'r') as file:
    HERO = json.load(file)


def profile_exist(player_id):
    url = f"https://api.opendota.com/api/players/{player_id}/recentMatches"
    response = requests.get(url)
    data = response.json()[0:20]
    return data


def get_heroes(player_id):
    url = f"https://api.opendota.com/api/players/{player_id}/heroes"
    response = requests.get(url)
    data = response.json()[:3]
    info = {}
    for obj in data:
        if obj['games']:
            hero = HERO[str(obj['hero_id'])]
            info[hero] = \
            {
                'games': obj['games'],
                'winrate': f"{round(100*obj['win']/obj['games'], 2)}%"
            }
    return info


def get_matches(player_id, data):
    tmp = {}
    for match in data:
        hero = HERO[str(match['hero_id'])]
        if bool(match['player_slot'] in range(1, 6)) == bool(match['radiant_win']):
            win = True
        else:
            win = False
        if hero not in tmp.keys():
            tmp[hero] = \
            {
                'win': 0,
                'total': 0
            }
        if win:
            tmp[hero]['win'] += 1
        tmp[hero]['total'] += 1
    info = {}
    for key in tmp.keys():
        if tmp[key]['total'] > 4:
            info[key] = {}
            info[key]['total'] = tmp[key]['total']
            info[key]['winrate'] = f"{round(100*tmp[key]['win']/tmp[key]['total'], 2)}%"
    return info


def get_wl(player_id):
    url = f"https://api.opendota.com/api/players/{player_id}/wl"
    response = requests.get(url)
    data = response.json()
    info = \
    {
        'games': data['win'] + data['lose'],
        'winrate': f"{round(100*data['win']/(data['win']+data['lose']), 2)}%"
    }
    return info


def get_info(player_id):
    data = profile_exist(player_id)
    if data:
        player = \
        {
            'link': f"https://www.opendota.com/players/{player_id}",
            'stats': get_wl(player_id),
            'heroes': get_heroes(player_id),
            'matches': get_matches(player_id, data)
        }
    else:
        player = {}
    return player


def get_players():
    path = f'/home/{os.getlogin()}/.steam/steam/steamapps/common/dota 2 beta/game/dota/server_log.txt'
    with open(path, 'r') as file:
        string = file.read()
    return list(map(int, re.findall('U:1:(\d+)', \
        re.findall('DOTA_GAMEMODE_ALL_DRAFT (.*)', string)[-1])))


def to_console(data):
    k = 0
    for id in data.keys():
        k += 1
        obj = data[id]
        if obj:
            print(f"[{k}]:\n{obj['link']}")
            print(f"g: {obj['stats']['games']} | wr: {obj['stats']['winrate']}")
            print('[Heroes]'.center(40))
            for hero in obj['heroes'].keys():
                txt = f"{hero}"
                txt = txt.center(20)
                print(f"{txt} | {obj['heroes'][hero]['winrate']}")
            print('[Spamming]'.center(40))
            for hero in obj['matches'].keys():
                txt = f"{hero}"
                txt = txt.center(20)
                print(f"{txt} | {obj['matches'][hero]['winrate']}")
            print('-----')


def to_html(data):
    html_page = '''
<!DOCTYPE HTML>
<html>
 <head>
  <meta charset="utf-8">
  <title>D2Track</title>
  <style>
    #window {
        width: 1000px;
        position: absolute;
        height: 565px;
        overflow: hidden;
    }
    #half {
        float: left;
        width: 500px;
        position: relative;
        height: 565px;
        overflow: hidden;
    }
    #profile {
        color: white;
        text-shadow: black 0 0 4px;
        width: 494px;
        position: relative;
        height: 17vh;
        border: 1px solid #000;
        margin: 2px;
        overflow: hidden;
    }
    #link {
        float: left;
        font-size: 12pt;
        text-align:  center;
        width: 120px;
        position: relative;
        height: 100%;
        border: 1px solid #000;
        overflow: hidden;
    }
    #hero {
        float: left;
        font-size: 11pt;
        text-align:  center;
        width: 70px;
        position: relative;
        height: 100%;
        border: 1px solid #000;
        overflow: hidden;
    }
    #last {
        float: left;
        font-size: 13pt;
        text-align:  center;
        width: 154px;
        position: relative;
        height: 100%;
        border: 1px solid #000;
        overflow: hidden;
    }
 </style>
 </head>
 <body background="bg.jpg" link="red" vlink="#cecece" alink="#ff0000">
  <div id="window">
    <div id="half">'''
    k = 0
    for id in data.keys():
        k += 1
        if k == 6:
            html_page += '''
    </div>
    <div id="half">'''
        obj = data[id]
        if not obj:
            html_page += '''
     <div id="profile">
      Неизвестно...
     </div>'''
        else:
            html_page += f'''
      <div id="profile">
        <div id="link">
          <br>
          <a href="{obj['link']}">
            Профиль
          </a>
          <br>
          Игр: {obj['stats']['games']}
          <br>
          Винрейт: {obj['stats']['winrate']}
        </div>'''
            h = 0
            hero_block = ''
            for hero in obj['heroes'].keys():
                h += 1
                heroname = hero.lower().replace(' ', '_')
                heroname = heroname.replace(' ', '_')
                html_page += f'''
        <div id="hero">
          <img src="https://api.opendota.com/apps/dota2/images/heroes/{heroname}_sb.png">
          Игр: {obj['heroes'][hero]['games']}
          <br>
          Винрейт: {obj['heroes'][hero]['winrate']}
        </div>'''
            html_page += (3-h) * '''
        <div id="hero">
        </div>'''
            html_page += '''
        <div id="last">
          Спамит:
          <br>'''
            for hero in obj['matches'].keys():
                heroname = hero.lower().replace(' ', '_')
                heroname = heroname.replace(' ', '_')
                html_page += f'<img src="https://api.opendota.com/apps/dota2/images/heroes/{heroname}_sb.png">'
            html_page += '''
        </div>
      </div>'''
    html_page += '''
    </div>
  </div>

 </body>
</html>'''
    with open('d2track.html', 'w') as file:
        file.write(html_page)


def main():
    data = {}
    players = get_players()
    for player_id in players:
        data[player_id] = get_info(player_id)
    to_html(data)
    to_console(data)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"{time.time()-start} seconds")