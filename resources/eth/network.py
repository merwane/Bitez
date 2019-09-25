from web3 import Web3
from config import INFURA_API_KEY, CRYPTO_NETWORK

def eth_network(net='testnet'): # CRYPTO_NETWORK
    if net == 'mainnet':
        url = 'https://mainnet.infura.io/v3/'+INFURA_API_KEY
    elif net == 'testnet':
        url = 'https://ropsten.infura.io/v3/'+INFURA_API_KEY

    web3 = Web3(Web3.HTTPProvider(url))
    return web3
