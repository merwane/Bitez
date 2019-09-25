from flask_restful import Resource, abort
from flask import request, jsonify
from services.dbconfig import Database
from resources.btc.prkey import decrypt
from services.api_calls import use_api_key
# btc
from resources.btc.balance import btc_balance
# bch
from resources.bch.balance import bch_balance
# eth
from resources.eth.balance import eth_balance

# init db
client = Database()
db = client.light()

class GetBalance(Resource):
    def get(self, coin):
        # verify api key
        api_key = request.args['api_key']
        currency = request.args['currency']
        use_api_key(api_key)
        # Bitcoin
        if coin == 'btc':
            # get and decrypt prkeys
            user = db.user.find_one({'api_keys.key': api_key}, {'username': True})
            wallet = db.wallet.find_one({'username': user['username']}, {'btc_wallet.prkey': True})
            enc_prkeys = []
            for prkey in wallet['btc_wallet']:
                enc_prkeys.append(prkey['prkey'])

            prkeys = []
            for prkey in enc_prkeys:
                prkeys.append(decrypt(str.encode(prkey)))
            
            balance = 0
            for prkey in prkeys:
                balance = balance + float(btc_balance(currency, prkey))
        # Bitcoin cash
        elif coin == 'bch':
            # get and decrypt prkeys
            user = db.user.find_one({'api_keys.key': api_key}, {'username': True})
            wallet = db.wallet.find_one({'username': user['username']}, {'bch_wallet.prkey': True})
            enc_prkeys = []
            for prkey in wallet['bch_wallet']:
                enc_prkeys.append(prkey['prkey'])

            prkeys = []
            for prkey in enc_prkeys:
                prkeys.append(decrypt(str.encode(prkey)))
            
            balance = 0
            for prkey in prkeys:
                balance = balance + float(bch_balance(currency, prkey))
        # Ethereum
        elif coin == 'eth':
            # get public address
            user = db.user.find_one({'api_keys.key': api_key}, {'username': True})
            wallet = db.wallet.find_one({'username': user['username']}, {'eth_wallet.address': True})
            balance = 0
            for address in wallet['eth_wallet']:
                balance = balance + float(eth_balance(address['address'], currency))
        return jsonify(network=coin.upper(), balance=balance, balance_currency=currency)
