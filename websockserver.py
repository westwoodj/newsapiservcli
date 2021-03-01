import asyncio
import websockets
import json
import pandas as pd
from newsapi import NewsApiClient


API_KEY="1562ed02072f49a193518d143d65603d"

newsApi = NewsApiClient(api_key=API_KEY)

def runAPI(datastream):

    data = newsApi.get_everything(q=datastream.get('q'), language=datastream.get('language'), sort_by=datastream.get('sort_by'), page_size=datastream.get('page_size'))


    articles = data['articles']

    df = pd.DataFrame(articles)

    #print(df)
    return df



async def echo(websocket, path):
    async for message in websocket:
        print("got message")
        data = json.loads(message)
        articles = runAPI(datastream=data)
        toSend = articles.to_json
        await websocket.send(toSend)

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()