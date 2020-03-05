"""
There are 2 functions to represent data

"""


def to_console(players, data, HEROES):
    k = 0
    for p_id in players:
        k += 1
        obj = data[p_id]
        print(f"[{k}]: {obj['name']}\n{obj['link']}")
        print(f"g: {obj['games']} | wr: {obj['winrate']}")
        print('[Heroes]'.center(40))
        for hero in obj['heroes']:
            txt = f"{HEROES[hero['hero_id']]['name']}"
            txt = txt.center(20)
            wr = round(100 * hero['win'] / hero['games'], 2)
            print(f"{txt} | {wr}%")
        print('[Spamming]'.center(40))
        for hero in obj['last_heroes']:
            txt = f"{HEROES[hero['hero_id']]['name']}"
            txt = txt.center(20)
            wr = round(100 * hero['win'] / hero['games'], 2)
            print(f"{txt} | {wr}%")
        print('-----')


def to_html(players, data, HEROES):
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
    for p_id in players:
        k += 1
        if k == 6:
            html_page += '''
    </div>
    <div id="half">'''
        obj = data[p_id]
        if obj["name"] == "Undefined":
            html_page += '''
     <div id="profile">
      Неизвестно...
     </div>'''
        else:
            html_page += f'''
      <div id="profile">
        <div id="link">
          <br>
          <a href="{obj['link']}" target="_blank">
            {obj['name']}
          </a>
          <br>
          Игр: {obj['games']}
          <br>
          Винрейт: {obj['winrate']}
        </div>'''
            h = 0
            hero_block = ''
            for hero in obj['heroes']:
                h += 1
                heroname = HEROES[hero['hero_id']]['name']
                dotaname = HEROES[hero['hero_id']]['dota_name']
                html_page += f'''
        <div id="hero">
          <img src="https://api.opendota.com/apps/dota2/images/heroes/{dotaname}_sb.png">
          Игр: {hero['games']}
          <br>
          Винрейт: {round(100 * hero['win'] / hero['games'], 2)}%
        </div>'''
            html_page += (3 - h) * '''
        <div id="hero">
        </div>'''
            html_page += '''
        <div id="last">
          Спамит:
          <br>'''
            for hero in obj['last_heroes']:
                heroname = HEROES[hero['hero_id']]['name']
                dotaname = HEROES[hero['hero_id']]['dota_name']
                html_page += f'<img src="https://api.opendota.com/apps/dota2/images/heroes/{dotaname}_sb.png">'
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
