Bitez: Self hosted cryptocurrency wallet as a service
==============================================

**Bitez** _(pronounced Bit Easy)_ is a self-hosted cryptocurrency wallet server you can use to create BTC/BCH/ETH wallets and perform multiple operations such as transactions and wallets generation with a simple HTTP interface.

You will need mongodb to store wallets, user accounts and api keys. Of course, private keys are encrypted before getting stored.

I created **Bitez** because I wanted a free alternative to [Block.io](https://block.io/).

<span style="color: red;"><strong>Important:</strong></span>
**Bitez** is still in alpha and therefore shouldn't be used for serving a large application with a large user base. Serving it for a small application is probably fine. I'm 20 and I'm broke so I don't want to be involved in any lawsuit haha

Installation
------------
After cloning this repository, you'll need to install all the dependencies:
```bash
# using pip
pip install requirements.txt

# or using Pipenv
pipenv install
```
Then you'll need to create a file at the root directory called (`.env`) with the following vars to store your secret environnement variables:
```bash
DB_HOST='<mongodb URI>'
DB_PORT='<mongodb port>'
DB_CLIENT='<mongodb client>'
SECRET_KEY='<random string used for jwt salting>'
MAIL_SERVER='<email smtp server>'
MAIL_PORT='<email smtp server port>'
MAIL_USERNAME='<email address for account activation>'
MAIL_PASSWORD='<password for accessing email account>'
ENCRYPTION_SECRET='<random string used for prkey encryption>'
INFURA_API_KEY='<infura API key>'
```
**Note:** You will need to create an [Infura](https://infura.io/) account to use ETH.

After saving the file, start the server with one of the following commands:
```bash
# mainnet server
python main.py

# or

# testnet server
python main.py --dev

# or

# mainnet production server
gunicorn main:app
```

## Guide

### Before accessing the API, you need to create an account and generate an API key:

### Account creation:
* Register:
```bash
curl -X POST /api/auth/register {
    "username":"<USERNAME>",
    "email":"<EMAIL>",
    "password":"<PASSWORD>"
}
```

* Activate account:
```bash
curl -X PUT /api/auth/activate {
    "activation_code":"<ACTIVATION_CODE>"
}
```

* Login to account:
```bash
# This will generate a JWT Token
curl -X GET /api/auth/login {
    "email":"<EMAIL>",
    "password":"<PASSWORD>"
}
```

* API key generation:
```bash
curl -X GET /api/generate_key
-H 'Authorization: jwt <JWT_TOKEN>'
```

* Get all API keys:
```bash
curl -X GET /api/keys
-H 'Authorization: jwt <JWT_TOKEN>'
```
#
### Generate a new address:
```bash
# BTC
curl -X GET /api/btc/generate?api_key=<API_KEY>

# BCH
curl -X GET /api/bch/generate?api_key=<API_KEY>

# ETH
curl -X GET /api/eth/generate?api_key=<API_KEY>
```

### Get all addresses:
```bash
# BTC
curl -X GET /api/btc/addresses?api_key=<API_KEY>

# BCH
curl -X GET /api/bch/addresses?api_key=<API_KEY>

# ETH
curl -X GET /api/eth/addresses?api_key=<API_KEY>
```

### Get wallet balance:
```bash
# BTC
curl -X GET /api/btc/balance?api_key=<API_KEY>&currency=<CURRENCY>

# BCH
curl -X GET /api/bch/balance?api_key=<API_KEY>&currency=<CURRENCY>

# ETH
curl -X GET /api/eth/balance?api_key=<API_KEY>&currency=<CURRENCY>

# available currencies: btc, bch, usd, eur, gbp, jpy and other major currencies like cad and chf
```

### Get transaction history:
```bash
# BTC
curl -X GET /api/btc/history?api_key=<API_KEY>

# BCH
curl -X GET /api/bch/history?api_key=<API_KEY>

# ETH (only returns txs number)
curl -X GET /api/eth/history?api_key=<API_KEY>
```

### Get current rates:
```bash
# BTC
curl -X GET /api/btc/rates?api_key=<API_KEY>&currency=<CURRENCY>

# BCH
curl -X GET /api/bch/rates?api_key=<API_KEY>&currency=<CURRENCY>

# ETH
curl -X GET /api/eth/rates?api_key=<API_KEY>&currency=<CURRENCY>

# available currencies: btc, bch, usd, eur, gbp, jpy and other major currencies like cad and chf
```

### Get a fiat amount in crypto:
```bash
# BTC
curl -X GET /api/btc/rates?api_key=<API_KEY>&currency=<CURRENCY>&amount=<AMOUNT>

# BCH
curl -X GET /api/bch/rates?api_key=<API_KEY>&currency=<CURRENCY>&amount=<AMOUNT>

# ETH
curl -X GET /api/eth/rates?api_key=<API_KEY>&currency=<CURRENCY>&amount=<AMOUNT>

# available currencies: btc, bch, usd, eur, gbp, jpy and other major currencies like cad and chf
```

### Check if an address is valid:
```bash
# BTC
curl -X GET /api/btc/validate?api_key=<API_KEY>&address=<ADDRESS>

# BCH
curl -X GET /api/bch/validate?api_key=<API_KEY>&address=<ADDRESS>

# ETH
curl -X GET /api/eth/validate?api_key=<API_KEY>&address=<ADDRESS>
```

### Perform a transaction:
```bash
# BTC
curl -X POST /api/btc/tx?api_key=<API_KEY>
-H 'Content-Type: application/json'
-d {
    "recipient":"<ADDRESS>",
    "amount": <AMOUNT>,
    "currency": "<CURRENCY>"
}

# BCH
curl -X POST /api/bch/tx?api_key=<API_KEY>
-H 'Content-Type: application/json'
-d {
    "recipient":"<ADDRESS>",
    "amount": <AMOUNT>,
    "currency": "<CURRENCY>"
}

# ETH
curl -X POST /api/eth/tx?api_key=<API_KEY>
-H 'Content-Type: application/json'
-d {
    "recipient":"<ADDRESS>",
    "amount": <AMOUNT>,
    "currency": "<CURRENCY>"
}

# available currencies: btc, bch, satoshi, usd, eur, gbp, jpy and other major currencies like cad and chf
```

Donate
------------

Based on community needs, I will keep improving the project and adding new functionalities. You can help me do that by **contributing** to the project or by **donating** a little something to encourage me.

**Donate BTC:** 1HHMRuezg1WAPqGRQ3S8xFKGgmMHZZrCoa

**Donate BCH:** bitcoincash:qrxjktfjdse3ll0ttrll20gykuhqjw764queg3w2tj

**Donate ETH:** 0xfA22ba67aBd32aa6c48795E535162Bd6B311636a

**Donate Love:** Just [tweet](https://twitter.com/merwanedr) me something cool :)

Contributing
------------
If you like **Bitez** and want to contribute to it, you can make a pull request on a new branch wether it is for a bugfix or for a new feature. 

You can also request a feature or report a bug by using Github issues, or by dropping me an [email](mailto:merwanedr@gmail.com).

Promoting the project is also considered a huge contribution! Any action is welcome as long as it helps **Bitez** grow! 

Notes and credits
------------
* I really wanted to thank [Ofek Lev](https://github.com/ofek) for his library [bit](https://github.com/ofek/bit) and [Sporestack](https://github.com/sporestack) with his fork [bitcash](https://github.com/sporestack/bitcash) which made **Bitez** possible without me having a headache!

* The rates and transaction API for BCH doesn't work on the testnet (dev server) because of a dependency issue. It should be fixed soon.

Changelog
------------
* **V0.0.1:** Added support for Bitcoin (BTC)
* **V0.0.2:** Added support for Bitcoin Cash (BCH)
* **V0.0.3:** Added support for Ethereum (ETH)
