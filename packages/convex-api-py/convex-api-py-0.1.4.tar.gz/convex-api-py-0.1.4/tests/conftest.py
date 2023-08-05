"""

    Conftest.py

"""

import logging
import pytest

from convex_api.account import Account
from convex_api.convex_api import ConvexAPI
from convex_api.utils import to_bytes

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('urllib3').setLevel(logging.INFO)

PRIVATE_TEST_KEY = 0x973f69bcd654b264759170724e1e30ccd2e75fc46b7993fd24ce755f0a8c24d0
PUBLIC_KEY = '0x5288Fec4153b702430771DFAC8AeD0B21CAFca4344daE0d47B97F0bf532b3306'
PRIVATE_KEY_MNEMONIC = 'now win hundred protect enroll cram stone come inch ill method often common quiz balance hundred negative truck crime turkey vague ecology nation balcony'

PRIVATE_TEST_KEY_TEXT = """
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIGbMFcGCSqGSIb3DQEFDTBKMCkGCSqGSIb3DQEFDDAcBAi3qm1zgjCO5gICCAAw
DAYIKoZIhvcNAgkFADAdBglghkgBZQMEASoEENjvj1nzc0Qy22L+Zi+n7yIEQMLW
o++Jzwlcg3PbW1Y2PxicdFHM3dBOgTWmGsvfZiLhSxTluXTNRCZ8ZLL5pi7JWtCl
JAr4iFzPLkM18YEP2ZE=
-----END ENCRYPTED PRIVATE KEY-----
"""
PRIVATE_TEST_KEY_PASSWORD = 'secret'

CONVEX_URL = 'https://convex.world'

TEST_ACCOUNT_NAME = 'test.convex-api'

@pytest.fixture(scope='module')
def test_account_info():
    return {
        'private_hex' : PRIVATE_TEST_KEY,
        'private_bytes': to_bytes(PRIVATE_TEST_KEY),
        'private_text': PRIVATE_TEST_KEY_TEXT,
        'private_password': PRIVATE_TEST_KEY_PASSWORD,
        'private_mnemonic': PRIVATE_KEY_MNEMONIC,
        'public_key': PUBLIC_KEY
    }

@pytest.fixture(scope='module')
def import_account(test_account_info):
    account = Account.import_from_bytes(test_account_info['private_bytes'])
    return account

@pytest.fixture(scope='module')
def test_account(convex, import_account):
    account = convex.setup_account(TEST_ACCOUNT_NAME, import_account)
    convex.topup_account(account)
    return account

@pytest.fixture(scope='module')
def convex_url():
    return CONVEX_URL

@pytest.fixture(scope='module')
def convex(convex_url):
    api = ConvexAPI(convex_url)
    return api

@pytest.fixture(scope='module')
def other_account(convex):
    account = convex.create_account()
    convex.topup_account(account)
    return account
