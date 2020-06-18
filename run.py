import os

from market_maker_keeper.oasis_market_maker_keeper import OasisMarketMakerKeeper


BASE_PATH = os.path.dirname(__file__)


# NETWORK = "mainnet"
NETWORK = "kovan"


if NETWORK.lower() == "kovan":
    RPC_HOST = "https://kovan.infura.io/v3/****"
    ETH_FROM = "0x0000000000000000000000000000000000000000"
    KEY_FILE = "/PATH/TO/KEY/FILE.json"
    PASS_FILE = "/PATH/TO/PASS/FILE.pass"

    # Market settings
    OASIS_ADDRESS = "0x3925970aE340255807dae79bfAd5C3b83F7aDB7b"
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
    ETH_FROM = "0x0000000000000000000000000000000000000000"
    KEY_FILE = "/PATH/TO/KEY/FILE.json"
    PASS_FILE = "/PATH/TO/PASS/FILE.pass"

    # Market settings
    OASIS_ADDRESS = "0x3925970aE340255807dae79bfAd5C3b83F7aDB7b"
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
else:
    raise Exception('NOT SUPPORTED NETWORK')


PRICE_FEED = "eth_rub-setzer"
CONFIG_FILE = "bands_mcr_eth.json"


if __name__ == '__main__':
    oasis_keeper_args = [
        '--rpc-host', RPC_HOST,

        '--eth-from', ETH_FROM,
        '--eth-key', f'key_file={KEY_FILE},pass_file={PASS_FILE}',

        '--price-feed', PRICE_FEED,
        '--oasis-address', OASIS_ADDRESS,

        '--buy-token-name', BUY_TOKEN["name"],
        '--buy-token-decimals', str(BUY_TOKEN["decimal"]),
        '--buy-token-address', BUY_TOKEN["address"],

        '--sell-token-name', SELL_TOKEN["name"],
        '--sell-token-decimals', str(SELL_TOKEN["decimal"]),
        '--sell-token-address', SELL_TOKEN["address"],

        '--config', os.path.join(BASE_PATH, 'bands', CONFIG_FILE),

        '--ethgasstation-api-key', "API_KEY_HERE"
        '--smart-gas-price'
        # '--debug',
        # '--telegram-log-config-file', os.path.join(BASE_PATH, 'telegram_conf.json')
    ]
    OasisMarketMakerKeeper(oasis_keeper_args).main()
