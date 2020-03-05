import aiohttp
import asyncio
import json
import os
import re
import requests
import time
from apihelper import *
from view import *


async def main():
    with open('heroes.json', 'r') as file:
        HEROES = json.load(file)
    data = {}
    tasks = []
    players = get_players()
    async with aiohttp.ClientSession() as session:
        for p_id in players:
            task = asyncio.create_task(get_data(p_id, data, session))
            tasks.append(task)
        await asyncio.gather(*tasks)
    #to_console(players, new, HEROES)
    to_html(players, data, HEROES)
    os.system('google-chrome --new-window -app d2track.html')


def test():
    t = time.time()
    asyncio.run(main())
    print("TOTAL TIME:", time.time() - t)


if __name__ == "__main__":
    asyncio.run(main())
