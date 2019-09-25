# eth gas fees in wei
import requests
from config import INFURA_API_KEY, CRYPTO_NETWORK


def eth_tx_fees():
    if CRYPTO_NETWORK == 'mainnet':
        net = 'https://mainnet.infura.io/v3/'+INFURA_API_KEY
    elif CRYPTO_NETWORK == 'testnet':
        net = 'https://ropsten.infura.io/v3/'+INFURA_API_KEY

    gas_price = requests.post(net, json={"jsonrpc":"2.0","method":"eth_gasPrice","params": [],"id":1})
    price = gas_price.json()
    return int(price['result'], 0)
