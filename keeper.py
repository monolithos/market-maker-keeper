import os
import uuid
import json

import web3

from market_maker_keeper.oasis_market_maker_keeper import OasisMarketMakerKeeper
from market_maker_keeper.uniswap_v2_market_maker import UniswapV2MarketMakerKeeper
from market_maker_keeper.mooniswap_market_maker import MooniswapMarketMakerKeeper


BASE_PATH = os.path.dirname(__file__)

MARKET_MAKER_TYPE = os.environ["MARKET_MAKER_TYPE"]


def generate_params_line(param_group: list):
    args = []
    for param in param_group:
        if param[1] is not None and not isinstance(param[1], (bool, list)):
            args.append(param[0])
            args.append(str(param[1]))
        elif isinstance(param[1], bool) and param[1]:
            args.append(param[0])
        elif isinstance(param[1], list) and len(param[1]) > 0 and param[1][0] is not None:

            for item in param[1]:
                args.append(param[0])
                args.append(str(item))
    return args


class EnvParam:
    value = None

    def __init__(self, env_name: str, cast_type, required, default=None):
        try:
            if cast_type in (list, set, tuple):
                self.value = cast_type(os.environ[env_name].split())
            else:
                self.value = cast_type(os.environ[env_name])
        except (TypeError, KeyError) as e:
            if required:
                raise Exception(f'Param {env_name} is required and must be cast to {str(cast_type)}')
            if cast_type in (list, set, tuple) and default is not None:
                self.value = cast_type([default])
            else:
                self.value = cast_type(default) if default is not None else None


def get_telegram_params():
    telegram_bot_token = EnvParam(env_name="TELEGRAM_BOT_TOKEN", cast_type=str, required=False).value

    if telegram_bot_token:
        chat_ids = {}
        ids = EnvParam(env_name="TELEGRAM_CHAT_IDS", cast_type=list, required=False, default=[]).value
        list(map(lambda x: chat_ids.update({x: x}), ids))
        telegram_conf_file = os.path.join(BASE_PATH, "telegram_conf.json")
        telegram_conf = {
            "bot_token": telegram_bot_token,
            "project_name": EnvParam(env_name="PROJECT_NAME", cast_type=str, required=False, default="monolithos_market_maker_keeper").value,
            "use_proxy": False,
            "request_kwargs": {
                "proxy_url": "",
                "urllib3_proxy_kwargs": {
                    "username": "",
                    "password": ""
                }
            },
            "chat_ids": chat_ids
        }
        with open(telegram_conf_file, "w") as file:
            file.write(json.dumps(telegram_conf))

        return [('--telegram-log-config-file', telegram_conf_file)]
    else:
        return []


if __name__ == '__main__':
    telegram_params = get_telegram_params()

    if MARKET_MAKER_TYPE in ['mooniswap', 'uniswap_v2', 'land']:
        password = str(uuid.uuid4())
        pk = EnvParam(env_name="ETH_PRIVATE_KEY", cast_type=str, required=True).value
        encrypt_pk = web3.Web3().eth.account.encrypt(private_key=pk, password=password)

        ETH_FROM = web3.Web3.toChecksumAddress(encrypt_pk["address"])
        P_ETH_FROM = EnvParam(env_name="ETH_FROM", cast_type=str, required=True).value

        if P_ETH_FROM.upper() != ETH_FROM.upper():
            raise Exception(f"private key does not match the ETH_FROM address ({P_ETH_FROM})")

        key_file = os.path.join(BASE_PATH, "key.json")
        pass_file = os.path.join(BASE_PATH, "pass.pass")
        with open(key_file, "w") as file:
            file.write(json.dumps(encrypt_pk))
        with open(pass_file, "w") as file:
            file.write(password)

        ETH_KEY = f'key_file={key_file},pass_file={pass_file}'

        network_params = [
            ('--rpc-host', EnvParam(env_name="RPC_HOST", cast_type=str, required=True).value),
            ('--eth-from', str(ETH_FROM)),
            ('--eth-key', str(ETH_KEY)),
            ('--rpc-timeout', EnvParam(env_name="RPC_TIMEOUT", cast_type=int, required=False).value),
        ]

        if MARKET_MAKER_TYPE == "land":

            bands = os.path.join(BASE_PATH, 'bands', EnvParam(env_name="BANDS", cast_type=str, required=True).value)

            token_params = [
                ('--buy-token-address', EnvParam(env_name="BUY_TOKEN_ADDRESS", cast_type=str, required=True).value),
                ('--buy-token-name', EnvParam(env_name="BUY_TOKEN_NAME", cast_type=str, required=True).value),
                ('--buy-token-decimals', EnvParam(env_name="BUY_TOKEN_DECIMALS", cast_type=str, required=True).value),

                ('--sell-token-address', EnvParam(env_name="SELL_TOKEN_ADDRESS", cast_type=str, required=True).value),
                ('--sell-token-name', EnvParam(env_name="SELL_TOKEN_NAME", cast_type=str, required=True).value),
                ('--sell-token-decimals', EnvParam(env_name="SELL_TOKEN_DECIMALS", cast_type=str, required=True).value),
            ]

            required_params = [
                ('--oasis-address', EnvParam(env_name="MARKET_ADDRESS", cast_type=str, required=True).value),
                ('--config', bands),
                ('--price-feed', EnvParam(env_name="PRICE_FEED", cast_type=str, required=True).value),
            ]

            optional_params = [
                ('--oasis-support-address', EnvParam(env_name="MARKET_SUPPORT_ADDRESS", cast_type=str, required=False).value),
                ('--price-feed-expiry', EnvParam(env_name="PRICE_FEED_EXPIRY", cast_type=int, required=False).value),
                ('--round-places', EnvParam(env_name="ROUND_PLACES", cast_type=int, required=False).value),
                ('--min-eth-balance', EnvParam(env_name="MIN_ETH_BALANCE", cast_type=float, required=False).value),

                ('--refresh-frequency', EnvParam(env_name="REFRESH_FREQUENCY", cast_type=int, required=False).value),
                ('--price-offset', EnvParam(env_name="PRICE_OFFSET", cast_type=float, required=False).value),
            ]

            ETHGASSTATION_API_KEY = EnvParam(env_name="ETHGASSTATION_API_KEY", cast_type=str, required=False).value
            is_smart_gas_price = ETHGASSTATION_API_KEY is not None
            gas_params = [
                ('--smart-gas-price', is_smart_gas_price),
                ('--ethgasstation-api-key', ETHGASSTATION_API_KEY),
                ('--gas-price', EnvParam(env_name="FIXED_GAS_PRICE", cast_type=int, required=False).value),
            ]

            keeper_args = generate_params_line(network_params)
            keeper_args += generate_params_line(required_params) + generate_params_line(optional_params)
            keeper_args += generate_params_line(token_params) + generate_params_line(gas_params)
            keeper_args += generate_params_line(telegram_params)
            OasisMarketMakerKeeper(keeper_args).main()
            print(f"OasisMarketMakerKeeper {keeper_args}")

        if MARKET_MAKER_TYPE == "uniswap_v2":
            token_params = [
                ('--first-token-address', EnvParam(env_name="FIRST_TOKEN_ADDRESS", cast_type=str, required=True).value),
                ('--first-token-name', EnvParam(env_name="FIRST_TOKEN_NAME", cast_type=str, required=True).value),
                ('--first-token-decimals', EnvParam(env_name="FIRST_TOKEN_DECIMALS", cast_type=str, required=True).value),

                ('--second-token-address', EnvParam(env_name="SECOND_TOKEN_ADDRESS", cast_type=str, required=True).value),
                ('--second-token-name', EnvParam(env_name="SECOND_TOKEN_NAME", cast_type=str, required=True).value),
                ('--second-token-decimals', EnvParam(env_name="SECOND_TOKEN_DECIMALS", cast_type=str, required=True).value),
            ]

            required_params = [
                ('--uniswap-router-address', EnvParam(env_name="ROUTER_ADDRESS", cast_type=str, required=True).value),
                ('--price-feed', EnvParam(env_name="PRICE_FEED", cast_type=str, required=True).value),
            ]

            optional_params = [
                ('--price-feed-expiry', EnvParam(env_name="PRICE_FEED_EXPIRY", cast_type=int, required=False).value),
                ('--max-delta-on-percent', EnvParam(env_name="ROUND_PLACES", cast_type=float, required=False).value),
                ('--max-first-token-amount-input', EnvParam(env_name="MAX_FIRST_TOKEN_INPUT", cast_type=float, required=False).value),
                ('--max-second-token-amount-input', EnvParam(env_name="MAX_SECOND_TOKEN_INPUT", cast_type=float, required=False).value),
                ('--min-eth-balance', EnvParam(env_name="MIN_ETH_BALANCE", cast_type=float, required=False).value),
                ('--min-first-token-balance', EnvParam(env_name="MIN_FIRST_TOKEN_BALANCE", cast_type=float, required=False).value),
                ('--min-second-token-balance', EnvParam(env_name="MIN_SECOND_TOKEN_BALANCE", cast_type=float, required=False).value),

                ('--refresh-frequency', EnvParam(env_name="REFRESH_FREQUENCY", cast_type=int, required=False).value),
            ]

            ETHGASSTATION_API_KEY = EnvParam(env_name="ETHGASSTATION_API_KEY", cast_type=str, required=False).value
            is_smart_gas_price = ETHGASSTATION_API_KEY is not None
            gas_params = [
                ('--smart-gas-price', is_smart_gas_price),
                ('--ethgasstation-api-key', ETHGASSTATION_API_KEY),
                ('--gas-price', EnvParam(env_name="FIXED_GAS_PRICE", cast_type=int, required=False).value),
            ]

            keeper_args = generate_params_line(network_params)
            keeper_args += generate_params_line(required_params) + generate_params_line(optional_params)
            keeper_args += generate_params_line(token_params) + generate_params_line(gas_params)
            keeper_args += generate_params_line(telegram_params)
            UniswapV2MarketMakerKeeper(keeper_args).main()
            print(f"UniswapV2MarketMakerKeeper {keeper_args}")

        if MARKET_MAKER_TYPE == "mooniswap":
            token_params = [
                ('--first-token-address', EnvParam(env_name="FIRST_TOKEN_ADDRESS", cast_type=str, required=True).value),
                ('--first-token-name', EnvParam(env_name="FIRST_TOKEN_NAME", cast_type=str, required=True).value),
                ('--first-token-decimals', EnvParam(env_name="FIRST_TOKEN_DECIMALS", cast_type=str, required=True).value),

                ('--second-token-address', EnvParam(env_name="SECOND_TOKEN_ADDRESS", cast_type=str, required=True).value),
                ('--second-token-name', EnvParam(env_name="SECOND_TOKEN_NAME", cast_type=str, required=True).value),
                ('--second-token-decimals', EnvParam(env_name="SECOND_TOKEN_DECIMALS", cast_type=str, required=True).value),
            ]

            required_params = [
                ('--mooniswap-factory-address', EnvParam(env_name="FACTORY_ADDRESS", cast_type=str, required=True).value),
                ('--price-feed', EnvParam(env_name="PRICE_FEED", cast_type=str, required=True).value),
            ]

            optional_params = [
                ('--price-feed-expiry', EnvParam(env_name="PRICE_FEED_EXPIRY", cast_type=int, required=False).value),
                ('--max-delta-on-percent', EnvParam(env_name="ROUND_PLACES", cast_type=float, required=False).value),
                ('--max-first-token-amount-input', EnvParam(env_name="MAX_FIRST_TOKEN_INPUT", cast_type=float, required=False).value),
                ('--max-second-token-amount-input', EnvParam(env_name="MAX_SECOND_TOKEN_INPUT", cast_type=float, required=False).value),
                ('--min-eth-balance', EnvParam(env_name="MIN_ETH_BALANCE", cast_type=float, required=False).value),
                ('--min-first-token-balance', EnvParam(env_name="MIN_FIRST_TOKEN_BALANCE", cast_type=float, required=False).value),
                ('--min-second-token-balance', EnvParam(env_name="MIN_SECOND_TOKEN_BALANCE", cast_type=float, required=False).value),

                ('--refresh-frequency', EnvParam(env_name="REFRESH_FREQUENCY", cast_type=int, required=False).value),
                ('--mooniswap-referral-address', EnvParam(env_name="REFERRAL_ADDRESS", cast_type=str, required=False).value),
            ]

            ETHGASSTATION_API_KEY = EnvParam(env_name="ETHGASSTATION_API_KEY", cast_type=str, required=False).value
            is_smart_gas_price = ETHGASSTATION_API_KEY is not None
            gas_params = [
                ('--smart-gas-price', is_smart_gas_price),
                ('--ethgasstation-api-key', ETHGASSTATION_API_KEY),
                ('--gas-price', EnvParam(env_name="FIXED_GAS_PRICE", cast_type=int, required=False).value),
            ]

            keeper_args = generate_params_line(network_params)
            keeper_args += generate_params_line(required_params) + generate_params_line(optional_params)
            keeper_args += generate_params_line(token_params) + generate_params_line(gas_params)
            keeper_args += generate_params_line(telegram_params)
            MooniswapMarketMakerKeeper(keeper_args).main()
            print(f"MooniswapMarketMakerKeeper {keeper_args}")

