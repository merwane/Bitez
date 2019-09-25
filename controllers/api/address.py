# TODO: add a label to each address
from flask_restful import Resource, abort
from flask import request, jsonify
from mongoengine import connect
from config import DB_HOST, DB_PORT, DB_CLIENT
from services.dbconfig import Database
from models.wallet import Wallet, BtcWallet, BchWallet, EthWallet
from services.api_calls import use_api_key
from resources.btc.prkey import encrypt
# btc
from resources.btc.network import btc_network
from resources.btc.generate import GenerateBtcKey
# bch
from resources.bch.network import bch_network
from resources.bch.generate import GenerateBchKey
# eth
from resources.eth.generate import GenerateEthKey

# init db
client = Database()
db = client.light()

# init mongoengine
connect(DB_CLIENT, host=DB_HOST, port=DB_PORT, retryWrites=False)

class GenerateAddr(Resource):
    def get(self, coin):
        # verify api key
        api_key = request.args['api_key']
        use_api_key(api_key)
        # Bitcoin
        if coin == 'btc':
            btc_key = GenerateBtcKey()
            btc_std_addr = btc_key.generate_std_addr()
            btc_wit_addr = btc_key.generate_wit_addr()
            btc_prkey = btc_key.generate_prkey()
            # encrypt and save prkey
            btc_prkey = encrypt(btc_prkey)
            btc_wallet = BtcWallet(
                    std_address = btc_std_addr,
                    wit_address = btc_wit_addr,
                    prkey = btc_prkey
                    )
            user = db.user.find_one({'api_keys.key': api_key}, {'username': True})
            wallet = Wallet.objects.get(username=user['username'])
            wallet.btc_wallet.append(btc_wallet)
            wallet.save()
            # reponse
            response = {
                    "network": "BTC",
                    "address": btc_std_addr,
                    "wit_address": btc_wit_addr
                    }

        # Bitcoin cash
        elif coin == 'bch':
            bch_key = GenerateBchKey()
            bch_std_addr = bch_key.generate_std_addr()
            bch_prkey = bch_key.generate_prkey()
            # encrypt and save prkey
            bch_prkey = encrypt(bch_prkey)
            bch_wallet = BchWallet(
                    address = bch_std_addr,
                    prkey = bch_prkey
                    )
            user = db.user.find_one({'api_keys.key': api_key}, {'username': True})
            wallet = Wallet.objects.get(username=user['username'])
            wallet.bch_wallet.append(bch_wallet)
            wallet.save()
            # reponse
            response = {
                    "network": "BCH",
                    "address": bch_std_addr,
                    }
        # Ethereum
        elif coin == 'eth':
            eth_key = GenerateEthKey()
            eth_std_addr = eth_key.generate_std_addr()
            eth_prkey = eth_key.generate_prkey()
            # encrypt and save prkey
            eth_prkey = encrypt(eth_prkey)
            eth_wallet = EthWallet(
                    address = eth_std_addr,
                    prkey = eth_prkey
                    )
            user = db.user.find_one({'api_keys.key': api_key}, {'username': True})
            wallet = Wallet.objects.get(username=user['username'])
            wallet.eth_wallet.append(eth_wallet)
            wallet.save()
            # response
            response = {
                    "network": "ETH",
                    "address": eth_std_addr
                    }
        else:
            abort(404, message="currency not found")
        return jsonify(status="success", data=response)


class GetAllAddr(Resource):
    def get(self, coin):
        # verify api key
        api_key = request.args['api_key']
        use_api_key(api_key)
        # Bitcoin
        if coin == 'btc':
            user = db.user.find_one({'api_keys.key': api_key}, {'username': True})
            wallet = db.wallet.find_one({'username': user['username']}, {'btc_wallet.prkey': False})
            user_addr = []
            for addr in wallet['btc_wallet']:
                user_addr.append(addr)
        # Bitcoin Cash
        elif coin == 'bch':
            user = db.user.find_one({'api_keys.key': api_key}, {'username': True})
            wallet = db.wallet.find_one({'username': user['username']}, {'bch_wallet.prkey': False})
            user_addr = []
            for addr in wallet['bch_wallet']:
                user_addr.append(addr)
        elif coin == 'eth':
            user = db.user.find_one({'api_keys.key': api_key}, {'username': True})
            wallet = db.wallet.find_one({'username': user['username']}, {'eth_wallet.prkey': False})
            user_addr = []
            for addr in wallet['eth_wallet']:
                user_addr.append(addr)
        else:
            abort(404, message="currency not found")
        return jsonify(addresses=user_addr)
