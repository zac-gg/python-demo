import asyncio
import aiohttp

P2P_Merchant_API = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/user/profile-and-ads-list?userNo=saa92019cb4cd3468b944299688b55f71'
P2P_Merchant_AD_NO = '11507424183435202560'


async def getP2PRate(session):
    response = await session.get(P2P_Merchant_API)
    response.raise_for_status()
    jsonData = await response.json()
    buyList = jsonData['data']['buyList']
    price = [ad['price']
             for ad in buyList if ad['advNo'] == P2P_Merchant_AD_NO][0]
    return price
