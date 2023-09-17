from binance.client import Client
from config import api_key, api_secret, asset_currency


def get_balance():
    """
    Функция проверки баланса, нигде не используется,
    просто лежит здесь чтобы использовать потом
    """
    client = None

    try:
        client = Client(api_key, api_secret)
        account_info = client.get_account()
        balances = {entry['asset']: entry['free'] for entry in account_info['balances']}

        for asset, balance in balances.items():
            if asset == asset_currency:
                balance_info = {
                    "balance": {
                        "asset": asset,
                        "balance": float(balance)
                    }
                }
                return balance_info

    except Exception as e:
        print(f"Ошибка получения баланса: {str(e)}")

    finally:
        if client:
            client.close_connection()
