import asyncio
import httpx
import json
import pandas as pd
import string
from bs4 import BeautifulSoup
from typing import Union

from . import columns


async def get_players(path: str = None):
    urls = [
        f'https://www.basketball-reference.com/players/{letter}/'
        for letter in string.ascii_lowercase
    ]
    async with httpx.AsyncClient() as client:
        resps = [client.get(url) for url in urls]
        player_pages = await asyncio.gather(*resps)
    players = {}
    for page in player_pages:
        soup = BeautifulSoup(page, 'lxml')
        for th in soup.find_all('th', {'data-stat': 'player'}):
            a = th.find('a')
            if a is None:
                continue
            player_name = a.text
            players[player_name] = a['href'].split('/')[-1][:-5]
    if path is not None:
        with open(path, 'w') as f:
            json.dump(players, f)
    return players


async def get_player_seasons(player: str) -> Union[pd.DataFrame, None]:
    url = f'https://www.basketball-reference.com/players/{player[0]}/{player}.html'
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        text = resp.text
    df = pd.read_html(text, attrs={'id': 'per_game'})
    if not df or len(df) != 1:
        return None
    df = df[0]
    mask = ~df['Age'].isna()
    df = df[mask]
    df = df.replace('Did Not Play', 0.0).replace('Inactive', 0.0)
    for col in columns.PLAYER_SEASON_BASIC_STATS:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df
