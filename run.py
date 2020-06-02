import os

from market_maker_keeper.oasis_market_maker_keeper import OasisMarketMakerKeeper


BASE_PATH = os.path.dirname(__file__)


RPC_HOST = "https://kovan.infura.io/v3/683836c8b9384898a9f99d483ae389bc"
ETH_FROM = "0xC0CCab7430aEc0C30E76e1dA596263C3bdD82932"
KEY_FILE = "/home/captain/development/dss-deploy-scripts/keystore.json,"
PASS_FILE = "/home/captain/development/dss-deploy-scripts/p.pass"

PRICE_FEED = "eth_rub-setzer"
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

CONFIG_FILE = "bands_mcr_eth.json"


if __name__ == '__main__':
    oasis_keeper_args = [
        '--rpc-host', 'https://kovan.infura.io/v3/683836c8b9384898a9f99d483ae389bc',

        '--eth-from', '0xC0CCab7430aEc0C30E76e1dA596263C3bdD82932',
        '--eth-key', f'key_file={KEY_FILE}pass_file={PASS_FILE}',

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
        # '--telegram-log-config-file', '/home/captain/development/makerdao_python/market-maker-keeper/telegram_conf.json'
    ]
    OasisMarketMakerKeeper(oasis_keeper_args).main()
