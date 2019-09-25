from dotenv import load_dotenv
from os.path import join, dirname
import os
import sys

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# config variables
try:
    ENVIRONMENT = sys.argv[1]
except IndexError:
    ENVIRONMENT = 'production'
# database
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))
DB_CLIENT = os.getenv('DB_CLIENT')

# jwt auth
SECRET_KEY = os.getenv('SECRET_KEY')
ACTIVATION_EXPIRE_DAYS = 5
TOKEN_EXPIRE_DAYS = 30

# email
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = int(os.getenv('MAIL_PORT'))
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')

# crypto network
if ENVIRONMENT == '--dev':
    CRYPTO_NETWORK = 'testnet'
else:
    CRYPTO_NETWORK = 'mainnet'

# encryption secrect
ENCRYPTION_SECRET = os.getenv('ENCRYPTION_SECRET')

# ethereum infura api key
INFURA_API_KEY = os.getenv('INFURA_API_KEY')
