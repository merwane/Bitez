from flask_restful import Resource, abort
from flask import request, jsonify
from services.dbconfig import Database
from resources.btc.prkey import decrypt
from services.api_calls import use_api_key
# btc
from resources.btc.history import btc_tx_history
# bch
from resources.bch.history import bch_tx_history
# eth
from resources.eth.history import eth_tx_count

# init db
client = Database()
db = client.light()

class GetHistory(Resource):
    def get(self, coin):
        # verify api key
        api_key = request.args['api_key']
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

            history = []
            for prkey in prkeys:
                history.append(btc_tx_history(prkey))
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

            history = []
            for prkey in prkeys:
                history.append(bch_tx_history(prkey))
        # Ethereum
        elif coin == 'eth':
            user = db.user.find_one({'api_keys.key': api_key}, {'username': True})
            wallet = db.wallet.find_one({'username': user['username']}, {'eth_wallet.address': True})
            history = 0
            for address in wallet['eth_wallet']:
                history = history + int(eth_tx_count(address['address'], 'latest'))
        return jsonify(transactions=history)
