# generate an address in a two formats (P2SH and WIT)
from resources.btc.network import btc_network

class GenerateBtcKey:
    def __init__(self):
        self.network = btc_network()
    
    def generate_prkey(self):
        return self.network.to_wif()

    def generate_std_addr(self):
        return self.network.address

    def generate_wit_addr(self):
        return self.network.segwit_address


