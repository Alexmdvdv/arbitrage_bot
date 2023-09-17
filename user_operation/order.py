import time
from binance.client import Client
from config import api_key, api_secret


def start_create_order(symbol, side, quantity, price):
    """
    Просто функция создания ордера, из необычного
    результат запрашивает через get_order каждые 0.2 сек,
    но запрашивается только в том случае если order_status != 'FILLED'
    """

    client = Client(api_key, api_secret)

    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            timeInForce="GTC",
            quantity=quantity,
            price=price
        )

        order_id = order['orderId']
        order_status = order['status']

        if order_status != 'FILLED':
            while True:
                order_info = client.get_order(
                    symbol=symbol,
                    orderId=order_id)
                if order_info['status'] == 'FILLED':
                    print(f'Ордер исполнен: {order_info}')
                    return order_info

                elif order_info['status'] == 'CANCELED':
                    return 'CANCELED'

                time.sleep(0.2)

        if order_status == 'CANCELED':
            return 'CANCELED'

        return order
    except Exception as e:
        print(f"Ошибка создания ордера: {e}")


def create_order(data):
    """
    Функция принимает список из 3х словарей,
    каждый словарь содержит всю необходимую информацию
    для создания ордера по указанной паре в словаре
    """
    for order_data in data:
        symbol = order_data['pair']
        side = order_data['side']
        quantity = order_data['quantity']
        price = order_data['price']

        order_status = start_create_order(symbol, side, quantity, price)
        quantity = str(order_status)
        print(quantity)

        if order_status == 'CANCELED':
            print(f'Ордер отменен: {order_status}')
            return

        if not order_status:
            print(f'Ордер не исполнен')
    return
