import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET_KEY')

asset_currency = os.getenv('ASSET')
procent_rate = os.getenv('RATE')

bal_btc = os.getenv('BTC')
bal_eth = os.getenv('ETH')
bal_usdt = os.getenv('USDT')
bal_fdusd = os.getenv('FDUSD')
bal_bnb = os.getenv('BNB')
bal_busd = os.getenv('BUSD')

limit1 = os.getenv('LIMIT1')
limit2 = os.getenv('LIMIT2')
