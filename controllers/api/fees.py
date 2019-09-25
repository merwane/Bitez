# get transactions fees for a given crypto
from flask_restful import Resource, abort
from flask import request, jsonify
from services.api_calls import use_api_key
# btc
from resources.btc.fees import btc_tx_fees
# bch
from resources.bch.fees import bch_tx_fees
# eth
from resources.eth.fees import eth_tx_fees

class GetTxFees(Resource):
    def get(self, coin):
        # verify api key
        api_key = request.args['api_key']
        use_api_key(api_key)
        # Bitcoin
        if coin == 'btc':
            unit = 'satoshis/byte'
            tx_fees = btc_tx_fees()
            tx_fees_fast = btc_tx_fees(fast=True)
        # Bitcoin cash
        elif coin == 'bch':
            unit = 'satoshis/byte'
            tx_fees = bch_tx_fees()
            tx_fees_fast = False
        # Ethereum
        elif coin == 'eth':
            unit = 'wei'
            tx_fees = eth_tx_fees()
            tx_fees_fast = False
        return jsonify(network=coin.upper(), unit=unit, tx_fees=tx_fees, tx_fees_fast=tx_fees_fast)
