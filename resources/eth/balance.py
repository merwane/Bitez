from resources.eth.network import eth_network
from resources.eth.rates import eth_to_fiat

def eth_balance(address, currency):
    web3 = eth_network()
    balance = web3.eth.getBalance(address)
    eth_balance = float(web3.fromWei(balance, "ether"))
    eth_balance = eth_to_fiat(eth_balance, currency)
    return eth_balance
