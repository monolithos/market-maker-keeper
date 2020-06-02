import os

from market_maker_keeper.oasis_market_maker_keeper import OasisMarketMakerKeeper


BASE_PATH = os.path.dirname(__file__)


if __name__ == '__main__':
    oasis_keeper_args = [
        '--rpc-host', 'https://kovan.infura.io/v3/683836c8b9384898a9f99d483ae389bc',

        '--eth-from', '0x6b383d7195bC26d6736124c7e77Db23a763ecDD1',
        '--eth-key', 'key_file=/home/captain/development/keystore/dd1_keystore.json,pass_file=/home/captain/development/keystore/dd1_pass.pass',

        '--price-feed', 'mdt_mcr-setzer',
        '--oasis-address', '0x3925970aE340255807dae79bfAd5C3b83F7aDB7b',

        '--buy-token-name', 'MCR',
        '--buy-token-decimals', '18',
        '--buy-token-address', '0xc2Dd906A7b72DEdEE0b1B4952b17005F0870B751',

        '--sell-token-name', 'MDT',
        '--sell-token-decimals', '18',
        '--sell-token-address', '0x532187039C9c7cC568B65aC07075e1a8b244e761',

        '--config', '/home/captain/development/makerdao_python/market-maker-keeper/bands/bands_mcr_mdt.json',

        '--ethgasstation-api-key', "API_KEY_HERE"
        '--smart-gas-price'
        # '--debug',
        # '--telegram-log-config-file', '/home/captain/development/makerdao_python/market-maker-keeper/telegram_conf.json'
    ]
    OasisMarketMakerKeeper(oasis_keeper_args).main()
