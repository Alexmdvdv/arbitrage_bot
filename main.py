import math
from binance import ThreadedWebsocketManager
from services.utils import check_json
from config import procent_rate, limit1, limit2, bal_btc, bal_eth, bal_usdt, bal_fdusd, bal_bnb, bal_busd
from user_operation.order import create_order

chains_info = check_json()

bal_btc = float(bal_btc)
bal_eth = float(bal_eth)
bal_usdt = float(bal_usdt)
bal_fdusd = float(bal_fdusd)
bal_bnb = float(bal_bnb)
bal_busd = float(bal_busd)

limit1 = int(limit1)
limit2 = int(limit2)

procent_rate = float(procent_rate)


def main():
    while True:
        twm = ThreadedWebsocketManager()
        twm.start()

        def socket_response(msg):
            last_prices = {}

            for item in msg:
                if 's' in item and 'c' in item:
                    symbol = item['s']
                    bid = item['b']
                    ask = item['a']
                    amount_deals = item['n']

                    last_prices[symbol] = (amount_deals, ask, bid)

            get_complete_data(last_prices)

        twm.start_ticker_socket(callback=socket_response)
        twm.join()


def get_complete_data(data):
    chains = []

    for chain in chains_info:
        item1 = chain['chain']['item1']
        item2 = chain['chain']['item2']
        item3 = chain['chain']['item3']
        step1 = chain['chain']['step1']
        step2 = chain['chain']['step2']
        step3 = chain['chain']['step3']

        asset = chain['chain']['asset']

        symbols_to_check = [item1, item2, item3]

        if all(symbol in data for symbol in symbols_to_check):
            deals1 = data[item1][0]
            deals2 = data[item2][0]
            deals3 = data[item3][0]
            price1 = data[item1][1]
            price2 = data[item2][1]
            price3 = data[item3][2]
            complete_data = {
                'item1': item1,
                'item2': item2,
                'item3': item3,

                'step1': step1,
                'step2': step2,
                'step3': step3,

                'deals1': deals1,
                'deals2': deals2,
                'deals3': deals3,

                'price1': price1,
                'price2': price2,
                'price3': price3,

                'asset': asset
            }

            chains.append(complete_data)

    get_calculated_data(chains)
    return


def get_calculated_data(datas):
    balance = None
    for data in datas:

        comm_rate1 = 0.001
        comm_rate2 = 0.001
        comm_rate3 = 0.001

        pair1 = data['item1']
        pair2 = data['item2']
        pair3 = data['item3']

        price1 = float(data['price1'])
        price2 = float(data['price2'])
        price3 = float(data['price3'])

        deals1 = data['deals1']
        deals2 = data['deals2']
        deals3 = data['deals3']

        step1 = float(data['step1'])
        step2 = float(data['step2'])

        order_price1 = data['price1']
        order_price2 = data['price2']
        order_price3 = data['price3']

        if deals1 > limit1 and deals2 > limit2 and deals3 > limit1:

            if data['asset'] == "BTC":
                balance = bal_btc
            if data['asset'] == "ETH":
                balance = bal_eth
            if data['asset'] == "BNB":
                balance = bal_bnb
            if data['asset'] == "BUSD":
                balance = bal_busd
            if data['asset'] == "USDT":
                balance = bal_usdt
            if data['asset'] == "FDUSD":
                balance = bal_fdusd

            gap1 = balance / price1
            sts1 = abs(int(math.log10(step1)))
            rg1 = math.floor(gap1 * 10 ** sts1) / 10 ** sts1
            cv1 = rg1 * comm_rate1
            res = rg1 - cv1
            rounded_result1 = math.floor(res * 10 ** sts1) / 10 ** sts1
            order_value1 = math.floor(gap1 * 10 ** sts1) / 10 ** sts1

            gap2 = rounded_result1 / price2
            sts2 = abs(int(math.log10(step2)))
            rg2 = math.floor(gap2 * 10 ** sts2) / 10 ** sts2
            cv2 = rg2 * comm_rate2
            res = rg2 - cv2
            rounded_result2 = math.floor(res * 10 ** sts2) / 10 ** sts2
            order_value2 = math.floor(gap2 * 10 ** sts2) / 10 ** sts2

            gap3 = rounded_result2 * price3
            commission_value3 = gap3 * comm_rate3
            rounded_result3 = gap3 - commission_value3

            calc_balance = order_value1 * price1
            difference = ((rounded_result3 - calc_balance) / calc_balance) * 100
            total = round(difference, 2)

            print(f'Цепочка: {pair1} | {pair2} | {pair3}')
            print(f'Цена: {price1} | {price2} | {price3}')
            print(f'Сделки: {deals1} | {deals2} | {deals3}')
            print(f'Количество: {order_value1} | {order_value2} | {rounded_result2}')
            print(f'Asset: {data["asset"]}')
            print(f'---------------------> {total} %')

            if total > procent_rate:
                order = [
                    {"pair": pair1, "price": order_price1, "quantity": order_value1, "side": "BUY"},
                    {"pair": pair2, "price": order_price2, "quantity": order_value2, "side": "BUY"},
                    {"pair": pair3, "price": order_price3, "quantity": rounded_result2, "side": "SELL"}
                ]

                print(f'Цепочка: {pair1} | {pair2} | {pair3}')
                print(f'Цена: {price1} | {price2} | {price3}')
                print(f'Сделки: {deals1} | {deals2} | {deals3}')
                print(f'Количество: {order_value1} | {order_value2} | {rounded_result2}')
                print(f'Asset: {data["asset"]}')
                print(f'---------------------> {total} %')

                create_order(order)
                return
    return


if __name__ == "__main__":
    main()
