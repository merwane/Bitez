from mongoengine import *
import datetime

class BtcWallet(EmbeddedDocument):
    std_address = StringField(unique=True)
    wit_address = StringField(unique=True)
    prkey = StringField(unique=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

class BchWallet(EmbeddedDocument):
    address = StringField(unique=True)
    prkey = StringField(unique=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

class EthWallet(EmbeddedDocument):
    address = StringField(unique=True)
    prkey = StringField(unique=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

class Wallet(Document):
    username = StringField(unique=True)
    btc_wallet = EmbeddedDocumentListField(BtcWallet)
    bch_wallet = EmbeddedDocumentListField(BchWallet)
    eth_wallet = EmbeddedDocumentListField(EthWallet)
