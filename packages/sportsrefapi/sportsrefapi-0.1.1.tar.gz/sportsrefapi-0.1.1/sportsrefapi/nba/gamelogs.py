import httpx
import pandas as pd
from typing import Union

from . import columns


async def get_gamelogs(player: str, year: int) -> Union[pd.DataFrame, None]:
    url = f'https://www.basketball-reference.com/players/{player[0]}/{player}/gamelog/{year}'
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        text = resp.text
    df = pd.read_html(text, attrs={'id': 'pgl_basic'})
    if not df or len(df) != 1:
        return None
    df = df[0]
    df['G'] = df['G'].fillna(0)
    mask = df['Rk'].astype(str).str.isnumeric() == True
    df = df[mask].drop('G', axis=1)
    df = df.replace('Did Not Play', 0.0).replace(
        'Inactive', 0.0).replace('Did Not Dress', 0.0)
    df = df.rename(columns={
        'Rk': 'G',
        'Unnamed: 5': 'H/A',
        'Unnamed: 7': 'W/L'
    })
    df[['W/L', 'Tm+/-']] = df['W/L'].str.split(expand=True)
    df['Tm+/-'] = df['Tm+/-'].str.slice(1, -1).astype(int)
    for col in columns.PLAYER_GAMELOG_BASIC_STATS:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'])
    return df
