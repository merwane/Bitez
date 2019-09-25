from resources.eth.network import eth_network

def eth_balance(address):
    web3 = eth_network()
    balance = web3.eth.getBalance(address)
    return float(web3.fromWei(balance, "ether"))
