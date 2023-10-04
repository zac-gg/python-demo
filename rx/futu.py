import asyncio
import aiohttp

FUTU_USDTHB_API = 'https://www.futunn.com/quote-api/quote-v2/get-stock-quote?stockId=72000227&marketType=11&marketCode=120&lotSize=100000&spreadCode=33&underlyingStockId=0&instrumentType=11'
FUTU_QUOTE_TOKEN = 'c0806e2152'


async def getUSD2THBRate(session):
    headers = {
        "Quote-Token": FUTU_QUOTE_TOKEN
    }
    response = await session.get(FUTU_USDTHB_API, headers=headers)
    response.raise_for_status()
    jsonData = await response.json()
    price = jsonData['data']['priceNominal']
    return price
