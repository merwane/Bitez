from web3.auto import w3

class GenerateEthKey:
    def __init__(self):
        self.key = w3.eth.account.create('KEYSMASH FJAFJKLDSKF7JKFDJ 1530')
    def generate_prkey(self):
        return self.key.privateKey.hex()
    def generate_std_addr(self):
        return self.key.address
        
