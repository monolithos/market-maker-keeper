import os

from market_maker_keeper.zrxv2_market_maker_keeper import ZrxExchangeV2


BASE_PATH = os.path.dirname(__file__)


NETWORK = "mainnet"
# NETWORK = "kovan"


if NETWORK.lower() == "kovan":
    RPC_HOST = "https://kovan.infura.io/v3/****"
    ETH_FROM = "0x0000000000000000000000000000000000000000"
    KEY_FILE = "/PATH/TO/KEY/FILE.json"
    PASS_FILE = "/PATH/TO/PASS/FILE.pass"

    # Market settings
    ZERO_X_EXCHANGE_ADDRESS = ""
    RELAYER_API_SERVER = 'https://api.0x.org/sra/'

    BUY_TOKEN = {
        "name": "MCR",
        "decimal": 18,
        "address": "0xEd1eC45E22e5D4AD23D6f60878549a8139A4B3AC"
    }

    SELL_TOKEN = {
        "name": "WETH",
        "decimal": 18,
        "address": "0xd0a1e359811322d97991e03f863a0c30c2cf029c"
    }
elif NETWORK.lower() == "mainnet":
    RPC_HOST = "https://mainnet.infura.io/v3/*******"
    ETH_FROM = ""
    KEY_FILE = "/home/captain/keystore/FILE.json"
    PASS_FILE = "/home/captain/keystore/FILE.pass"

    # Market settings
    RELAYER_API_SERVER = 'https://api.0x.org/sra/'
    ZERO_X_EXCHANGE_ADDRESS = "0x61935CbDd02287B511119DDb11Aeb42F1593b7Ef"

    BUY_TOKEN = {
        "name": "MCR",
        "decimal": 18,
        "address": "0xeD351575b9869AADA94435e0066ba38E08800b60"
    }

    SELL_TOKEN = {
        "name": "WETH",
        "decimal": 18,
        "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    }
else:
    raise Exception('NOT SUPPORTED NETWORK')


PRICE_FEED = "eth_rub-setzer"
CONFIG_FILE = "bands_mcr_eth.json"
ORDER_EXPIRY = 7200


if __name__ == '__main__':
    oasis_keeper_args = [
        '--rpc-host', RPC_HOST,

        '--eth-from', ETH_FROM,
        '--eth-key', f'key_file={KEY_FILE},pass_file={PASS_FILE}',

        '--price-feed', PRICE_FEED,
        '--exchange-address', ZERO_X_EXCHANGE_ADDRESS,
        '--relayer-api-server', RELAYER_API_SERVER,
        '--order-expiry', ORDER_EXPIRY,

        '--buy-token-decimals', str(BUY_TOKEN["decimal"]),
        '--buy-token-address', BUY_TOKEN["address"],

        '--sell-token-decimals', str(SELL_TOKEN["decimal"]),
        '--sell-token-address', SELL_TOKEN["address"],

        '--config', os.path.join(BASE_PATH, 'bands', CONFIG_FILE),

        '--ethgasstation-api-key', "API_KEY_HERE"
        '--smart-gas-price'
        # '--debug',
        # '--telegram-log-config-file', os.path.join(BASE_PATH, 'telegram_conf.json')
    ]
    ZrxExchangeV2(oasis_keeper_args).main()
