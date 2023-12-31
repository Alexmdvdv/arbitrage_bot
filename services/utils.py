import json
import os
import requests

"""Список всех котируемых валют которые используются в get_arbitrage_chain"""

asset_currency = ['BTC', 'ETH', 'BNB', 'BUSD', 'USDT', 'FDUSD']


def get_currency():
    """
    Функция делает запрос на url, получает всю инфу по всем существующим парам,
    перебирает полученную инфу и парсит необходимые данные
    """
    response = requests.get('https://api.binance.com/api/v3/exchangeInfo')
    exchange_info = response.json()

    symbol_info_list = []

    for symbol_data in exchange_info['symbols']:

        if symbol_data['status'] == 'TRADING':
            base_asset = symbol_data['baseAsset']
            quote_asset = symbol_data['quoteAsset']
            step_size = symbol_data['filters'][1]['stepSize']

            symbol_info_list.append({
                "symbol": symbol_data['symbol'],
                "base": base_asset,
                "quote": quote_asset,
                "step": step_size,
            })

    return get_arbitrage_chain(symbol_info_list)


def get_arbitrage_chain(symbol_data_list):
    """
    Функция получает список словарей symbol_data_list,
    после чего формирует цепочки в соответствии с условием,
    также добавляет всю необходимую информацию для них, включая шаг,
    котируемую валюту и название пары. (все данные упорядочены)
    Формирует список chains из получившихся цепочек и возвращает его же
    """
    chains = []

    for currency in asset_currency:

        for pair1 in symbol_data_list:

            base1 = pair1["base"]
            quote1 = pair1["quote"]
            step1 = pair1['step']

            for pair2 in symbol_data_list:
                base2 = pair2["base"]
                quote2 = pair2["quote"]
                step2 = pair2['step']

                for pair3 in symbol_data_list:
                    base3 = pair3["base"]
                    quote3 = pair3["quote"]
                    step3 = pair3['step']

                    if (base1 == quote2 and base2 == base3 and
                            quote1 == currency and quote3 == currency and quote1 == quote3):
                        chains.append({
                            "chain": {
                                "item1": pair1['symbol'],
                                "item2": pair2['symbol'],
                                "item3": pair3['symbol'],
                                "step1": step1,
                                "step2": step2,
                                "step3": step3,
                                "asset": currency
                            }
                        })

    return chains


def check_json():
    """
    Функция проверяет есть ли в currencys.json данные, если нет
    дергает функцию get_currency которая в свою очередь дергает
    get_arbitrage_chain которая возвращает chains. Соответственно это
    главная функция которая запускает механизм добавления данных в json.
    Если данные есть в json то просто возвращает эти данные.
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_directory, 'currencys.json')

    with open(json_path, 'r') as file:
        data = json.load(file)

    if not data:
        chains = get_currency()
        with open(json_path, 'w') as json_file:
            json.dump(chains, json_file, indent=4)

    return data


check_json()
