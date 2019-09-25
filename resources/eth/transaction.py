from resources.eth.network import eth_network
from resources.eth.rates import fiat_to_eth

def eth_tx(amount, currency, recipient, sender, prkey):
    # currency conversion
    eth_amount = fiat_to_eth(amount, currency)
    # tx
    w3 = eth_network()
    signed_txn = w3.eth.account.signTransaction(dict(
    nonce=w3.eth.getTransactionCount(sender),
    gasPrice = w3.eth.gasPrice, 
    gas = 100000,
    to=recipient,
    value=w3.toWei(float(eth_amount),'ether')                          
    ), prkey)
    
    tx = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    return tx
