import requests

def eth_to_fiat(amount, currency):
    rates = requests.get('https://api.coinbase.com/v2/exchange-rates?currency=ETH')
    rates_eth = rates.json()
    return float(rates_eth['data']['rates'][currency.upper()]) * amount

def fiat_to_eth(amount, currency):
    rates = requests.get('https://api.coinbase.com/v2/exchange-rates?currency='+currency.upper())
    rates_curr = rates.json()
    rate = float(rates_curr['data']['rates']['ETH']) * amount
    return str(rate)
