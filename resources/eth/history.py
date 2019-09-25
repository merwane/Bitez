# tx count
import requests
from config import INFURA_API_KEY, CRYPTO_NETWORK

# block param: loop 'latest', 'pending'
def eth_tx_count(address, block):
    if CRYPTO_NETWORK == 'mainnet':
        net = 'https://mainnet.infura.io/v3/'+INFURA_API_KEY
    elif CRYPTO_NETWORK == 'testnet':
        net = 'https://ropsten.infura.io/v3/'+INFURA_API_KEY

    hist = requests.post(net, json={"jsonrpc":"2.0","method":"eth_getTransactionCount","params": [address, block],"id":1})
    txs = hist.json()
    return int(txs['result'], 0)
