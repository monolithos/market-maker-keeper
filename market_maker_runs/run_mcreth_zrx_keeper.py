import os

from market_maker_keeper.zrxv3_market_maker_keeper import ZrxV3MarketMakerKeeper


BASE_PATH = os.path.dirname(__file__)


# NETWORK = "mainnet"
NETWORK = "kovan"


if NETWORK.lower() == "kovan":
    RPC_HOST = "https://kovan.infura.io/v3/e13a288dfcde4e7bbe2c7bd5a7ee21da"
    ETH_FROM = "0xC0CCab7430aEc0C30E76e1dA596263C3bdD82932"
    KEY_FILE = "/home/captain/development/keystore/9ae_keystore.json"
    PASS_FILE = "/home/captain/development/keystore/9ae_pass.pass"

    # Market settings
    ZERO_X_EXCHANGE_ADDRESS = "0x4eacd0af335451709e1e7b570b8ea68edec8bc97"
    RELAYER_API_SERVER = 'https://kovan.api.0x.org/sra'

    BUY_TOKEN = {
        "name": "MCR",
        "decimal": 18,
        "address": "0xB19E3176C7967012755e1F2320623c20f9Da410b"
    }

    SELL_TOKEN = {
        "name": "WETH",
        "decimal": 18,
        "address": "0xd0a1e359811322d97991e03f863a0c30c2cf029c"
    }
elif NETWORK.lower() == "mainnet":
    RPC_HOST = "https://mainnet.infura.io/v3/e13a288dfcde4e7bbe2c7bd5a7ee21da"
    ETH_FROM = "0x8426B3abdBAe6A4815342CDcef7014C1671f17FE"
    KEY_FILE = "/home/captain/development/keystore/7fe_keystore.json"
    PASS_FILE = "/home/captain/development/keystore/7fe_pass.pass"

    # Market settings
    RELAYER_API_SERVER = 'https://api.0x.org/sra'
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


# PRICE_FEED = "eth_rub-setzer"
PRICE_FEED = "fixed:17000"
CONFIG_FILE = "bands_mcr_eth.json"
ORDER_EXPIRY = "7200"


if __name__ == '__main__':
    zrx_keeper_args = [
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
    ZrxV3MarketMakerKeeper(zrx_keeper_args).main()
