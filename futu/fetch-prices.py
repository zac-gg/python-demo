import asyncio
import aiohttp
import time
import csv

FUTU_USDTHB_API = 'https://www.futunn.com/quote-api/quote-v2/get-stock-quote?stockId=72000227&marketType=11&marketCode=120&lotSize=100000&spreadCode=33&underlyingStockId=0&instrumentType=11'
P2P_Merchant_API = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/user/profile-and-ads-list?userNo=saa92019cb4cd3468b944299688b55f71'
P2P_SEARCH_API = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

FUTU_QUOTE_TOKEN = 'c0806e2152'
P2P_Merchant_AD_NO = '11507424183435202560'

CSV_FILE = 'exchange_rates.csv'

async def get_futu_rate(session: aiohttp.ClientSession):
    headers = {
        "Quote-Token": FUTU_QUOTE_TOKEN
    }
    response = await session.get(FUTU_USDTHB_API, headers=headers)
    response.raise_for_status()
    jsonData = await response.json()

    price = jsonData['data']['priceNominal']
    print('Futu Price: {}'.format(price))
    return price

async def get_p2p_rate(session: aiohttp.ClientSession):
    response = await session.get(P2P_Merchant_API)
    response.raise_for_status()
    jsonData = await response.json()

    buyList = jsonData['data']['buyList']
    price = [ad['price'] for ad in buyList if ad['advNo'] == P2P_Merchant_AD_NO][0]
    print('P2P Ad Price: {}'.format(price))
    return price

async def get_p2p_best_price(session: aiohttp.ClientSession):
    parameters = {
        'asset': 'USDT',
        'classifies': ['mass', 'profession'],
        'countries': [],
        'fiat': 'THB',
        'page': 1,
        'payTypes': [],
        'proMerchantAds': False,
        'rows': 10,
        'shieldMerchantAds': False,
        'tradeType': 'SELL'
    }
    response = await session.post(P2P_SEARCH_API, json=parameters)
    response.raise_for_status()
    jsonData = await response.json()

    bestPriceAd = jsonData['data'][0]['adv']
    return bestPriceAd

async def get_rates():
    async with aiohttp.ClientSession() as session:
        rate_futu, rate_p2p, bestPriceAd = await asyncio.gather(
            get_futu_rate(session),
            get_p2p_rate(session),
            get_p2p_best_price(session)
        )
        return rate_futu, rate_p2p, bestPriceAd

def write_to_csv(query_time, lastPrice, rate_futu, rate_p2p, bestPriceAd):
    price_futu = float(rate_futu)
    price_p2p = float(rate_p2p)
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        isBestPrice = 'Ture' if bestPriceAd['advNo'] == P2P_Merchant_AD_NO else 'No, Best Price is {}'.format(bestPriceAd['price'])
        riseRate = '-' if lastPrice == '-' else '{:.2%}'.format((price_futu - float(lastPrice)) / float(lastPrice))
        writer.writerow([query_time, price_futu, riseRate, price_p2p, isBestPrice, price_p2p / price_futu, price_p2p - price_futu])

async def main():
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Time', 'Futu USD/THB Price (A)', 'USD/THB Price Change', 'P2P Ad Price (B)', 'Is Best Price in P2P', 'Auto Pricing Strategy (B/A)', 'Auto Pricing Strategy (B-A)'])

    lastPrice = '-'
    while True:
        query_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print('----------------------')
        print('Query Time: {}'.format(query_time))
        rate_futu, rate_p2p, bestPriceAd = await get_rates()
        print('----------------------')
        write_to_csv(query_time, lastPrice, rate_futu, rate_p2p, bestPriceAd)
        lastPrice = rate_futu
        await asyncio.sleep(10)

asyncio.run(main())
