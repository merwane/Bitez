from flask_restful import Resource, abort
from flask import request, jsonify
from services.api_calls import use_api_key
# btc
from resources.btc.valid import btc_addr_is_valid
# bch
from resources.bch.valid import bch_addr_is_valid
# eth
from resources.eth.valid import eth_addr_is_valid

class ValidAddr(Resource):
    def get(self, coin):
        # verify api key
        api_key = request.args['api_key']
        address = request.args['address']
        use_api_key(api_key)
        # Bitcoin
        if coin == 'btc':
            valid = btc_addr_is_valid(address)
        # Bitcoin cash
        elif coin == 'bch':
            valid = bch_addr_is_valid(address)
        # Ethereum
        elif coin == 'eth':
            valid = eth_addr_is_valid(address)
        return jsonify(network=coin.upper(), address=address, is_valid=valid)
