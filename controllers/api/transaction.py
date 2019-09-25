from flask_restful import Resource, abort
from flask import request, jsonify
from services.dbconfig import Database
from resources.btc.prkey import decrypt
from services.api_calls import use_api_key
# btc
from resources.btc.transaction import btc_tx
from resources.btc.valid import btc_addr_is_valid
# bch
from resources.bch.transaction import bch_tx
from resources.bch.valid import bch_addr_is_valid
# eth
from resources.eth.transaction import eth_tx
from resources.eth.valid import eth_addr_is_valid

# init db
client = Database()
db = client.light()

class Transaction(Resource):
    def post(self, coin):
        # verify api key
        api_key = request.args['api_key']
        recipient = request.json['recipient']
        amount = request.json['amount']
        currency = request.json['currency']
        use_api_key(api_key)
        # Bitcoin
        if coin == 'btc':
            # validate recipient address
            if btc_addr_is_valid(recipient) == False:
                abort(400, message="Recipient\'s address not valid")
            # get and decrypt prkeys
            user = db.user.find_one({'api_keys.key': api_key}, {'username': True})
            wallet = db.wallet.find_one({'username': user['username']}, {'btc_wallet.prkey': True})
            enc_prkeys = []
            for prkey in wallet['btc_wallet']:
                enc_prkeys.append(prkey['prkey'])

            prkeys = []
            for prkey in enc_prkeys:
                prkeys.append(decrypt(str.encode(prkey)))

            for prkey in prkeys:
                tx = btc_tx(recipient, amount, currency, prkey)
                if tx != False:
                    break
            
            if tx == False:
                status = 'failed'
            else:
                status = 'success'
        # Bitcoin cash
        elif coin == 'bch':
            # validate recipient address
            if bch_addr_is_valid(recipient) == False:
                abort(400, message="Recipient\'s address not valid")
            # get and decrypt prkeys
            user = db.user.find_one({'api_keys.key': api_key}, {'username': True})
            wallet = db.wallet.find_one({'username': user['username']}, {'bch_wallet.prkey': True})
            enc_prkeys = []
            for prkey in wallet['bch_wallet']:
                enc_prkeys.append(prkey['prkey'])

            prkeys = []
            for prkey in enc_prkeys:
                prkeys.append(decrypt(str.encode(prkey)))

            for prkey in prkeys:
                tx = bch_tx(recipient, amount, currency, prkey)
                if tx != False:
                    break
            
            if tx == False:
                status = 'failed'
            else:
                status = 'success'
        # Ethereum
        elif coin == 'eth':
            # validate recipient address
            if eth_addr_is_valid(recipient) == False:
                abort(400, message="Recipient\'s address not valid")
            # get and decrypt prkeys
            user = db.user.find_one({'api_keys.key': api_key}, {'username': True})
            wallet = db.wallet.find_one({'username': user['username']}, {'eth_wallet.address': True, 'eth_wallet.prkey': True})

            enc_prkeys = []
            for prkey in wallet['eth_wallet']:
                enc_prkeys.append(prkey['prkey'])
            
            prkeys = []
            for prkey in enc_prkeys:
                prkeys.append(decrypt(str.encode(prkey)))
            
            addresses = []
            for address in wallet['eth_wallet']:
                addresses.append(address['address'])
            
            for address, prkey in zip(addresses, prkeys):
                tx = eth_tx(amount, currency, recipient, sender=address, prkey=prkey)
                if tx != False:
                    break

            if tx == False:
                status = 'failed'
            else:
                status = 'success'
                tx = str(tx.hex())

        return jsonify(status=status, transaction_id=tx, recipient=recipient, amount=amount, currency=currency.upper(), network=coin.upper())
