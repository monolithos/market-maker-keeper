from market_maker_keeper.oasis_market_maker_keeper import OasisMarketMakerKeeper


if __name__ == '__main__':
    oasis_keeper_args = [
        '--rpc-host', 'https://kovan.infura.io/v3/683836c8b9384898a9f99d483ae389bc',

        '--eth-from', '0xC0CCab7430aEc0C30E76e1dA596263C3bdD82932',
        '--eth-key', 'key_file=/home/captain/development/dss-deploy-scripts/keystore.json,pass_file=/home/captain/development/dss-deploy-scripts/p.pass',

        '--price-feed', 'eth_rub-setzer',
        '--oasis-address', '0x43db77b8c4C843a76E3728D4A1E61F1DfDE22219',

        '--buy-token-name', 'MCR',
        '--buy-token-decimals', '18',
        '--buy-token-address', '0xEd1eC45E22e5D4AD23D6f60878549a8139A4B3AC',

        '--sell-token-name', 'WETH',
        '--sell-token-decimals', '18',
        '--sell-token-address', '0xd0a1e359811322d97991e03f863a0c30c2cf029c',

        '--config', '/home/captain/development/makerdao_python/market-maker-keeper/bands/bands_mcr_eth.json',

        '--ethgasstation-api-key', "API_KEY_HERE"
        '--smart-gas-price'
        '--debug',
        # '--telegram-log-config-file', '/home/captain/development/makerdao_python/market-maker-keeper/telegram_conf.json'
    ]
    OasisMarketMakerKeeper(oasis_keeper_args).main()
