# This file is part of Maker Keeper Framework.
#
# Copyright (C) 2017-2018 reverendus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import logging
import sys
# import time
from math import sqrt
# from typing import List

from attrdict import AttrDict
from web3 import Web3, HTTPProvider

from market_maker_keeper.gas import GasPriceFactory
# from market_maker_keeper.order_book import OrderBookManager
from market_maker_keeper.price_feed import PriceFeedFactory
from market_maker_keeper.util import setup_logging

from pymaker import Address, Transact
from pymaker.approval import directly
from pymaker.keys import register_keys
from pymaker.lifecycle import Lifecycle
from pymaker.numeric import Wad
from pymaker.model import Token

from pymaker.token import ERC20Token
from pymaker.util import eth_balance

from pymaker.uniswap_v2 import UniswapRouter


class UniswapSetPriceTransaction:
    market_price: Wad
    first_token: Address
    second_token: Address
    max_delta_on_percent: int

    def __init__(self, market_price: Wad, first_token: Address, second_token: Address, max_delta_on_percent: int):
        self.market_price = market_price
        self.first_token = first_token
        self.second_token = second_token
        self.max_delta_on_percent = max_delta_on_percent


class UniswapV2MarketMakerKeeper:
    """Keeper acting as a market maker on Uniswap v2."""

    logger = logging.getLogger()
    send_transaction: bool = False

    def add_arguments(self, parser):
        """Provider info"""
        parser.add_argument("--rpc-host", type=str, default="http://localhost:8545",
                            help="JSON-RPC host (default: `http://localhost:8545`)")

        parser.add_argument("--rpc-timeout", type=int, default=10,
                            help="JSON-RPC timeout (in seconds, default: 10)")

        parser.add_argument("--eth-from", type=str, required=True,
                            help="Ethereum account from which to send transactions")

        parser.add_argument("--eth-key", type=str, nargs='*',
                            help="Ethereum private key(s) to use (e.g. 'key_file=aaa.json,pass_file=aaa.pass')")

        """Exchange info"""
        parser.add_argument("--uniswap-router-address", type=str, required=True,
                            help="Ethereum address of the Uniswap Router v2 contract")

        """Tokens info"""
        parser.add_argument("--first-token-address", type=str, required=True,
                            help="Ethereum address of the first token")

        parser.add_argument("--first-token-name", type=str, required=True,
                            help="name of the first token")

        parser.add_argument("--first-token-decimals", type=int, required=True,
                            help="decimal of the first token")

        parser.add_argument("--second-token-address", type=str, required=True,
                            help="Ethereum address of the second token")

        parser.add_argument("--second-token-name", type=str, required=True,
                            help="name of the second token")

        parser.add_argument("--second-token-decimals", type=int, required=True,
                            help="decimal of the second token")

        """settings"""
        parser.add_argument("--price-feed", type=str, required=True,
                            help="Source of price feed")

        parser.add_argument("--price-feed-expiry", type=int, default=120,
                            help="Maximum age of the price feed (in seconds, default: 120)")

        parser.add_argument("--max-delta-on-percent", type=float, default=3,
                            help="Delta permissible margin")

        parser.add_argument("--max-first-token-amount-input", type=float, default=10000,
                            help="The maximum allowed number of first tokens that can be exchanged for installation.")

        parser.add_argument("--max-second-token-amount-input", type=float, default=10000,
                            help="The maximum allowed number of second tokens that can be exchanged for installation.")

        parser.add_argument("--min-eth-balance", type=float, default=0,
                            help="Minimum ETH balance below which keeper will cease operation")

        parser.add_argument("--min-first-token-balance", type=float, default=0,
                            help="Minimum first token balance")

        parser.add_argument("--min-second-token-balance", type=float, default=0,
                            help="Minimum second token balance")

        parser.add_argument("--gas-price", type=int, default=50000000000,
                            help="Gas price (in Wei)")

        parser.add_argument("--smart-gas-price", dest='smart_gas_price', action='store_true',
                            help="Use smart gas pricing strategy, based on the ethgasstation.info feed")

        parser.add_argument("--ethgasstation-api-key", type=str, default=None, help="ethgasstation API key")

        parser.add_argument("--refresh-frequency", type=int, default=10,
                            help="Order book refresh frequency (in seconds, default: 10)")

        parser.add_argument("--debug", dest='debug', action='store_true',
                            help="Enable debug output")

        parser.add_argument("--telegram-log-config-file", type=str, required=False,
                            help="config file for send logs to telegram chat (e.g. 'telegram_conf.json')", default=None)

        parser.add_argument("--keeper-name", type=str, required=False,
                            help="market maker keeper name (e.g. 'Uniswap_V2_MDTETH')", default="Uniswap_V2")

    def __init__(self, args: list, **kwargs):
        parser = argparse.ArgumentParser(prog='uniswap-market-maker-keeper')
        self.add_arguments(parser=parser)
        self.arguments = parser.parse_args(args)
        setup_logging(self.arguments)

        provider = HTTPProvider(endpoint_uri=self.arguments.rpc_host,
                                request_kwargs={'timeout': self.arguments.rpc_timeout})
        self.web3: Web3 = kwargs['web3'] if 'web3' in kwargs else Web3(provider)

        self.web3.eth.defaultAccount = self.arguments.eth_from
        register_keys(self.web3, self.arguments.eth_key)
        self.our_address = Address(self.arguments.eth_from)

        self.uniswap_router = UniswapRouter(web3=self.web3, router=Address(self.arguments.uniswap_router_address))

        self.first_token = ERC20Token(web3=self.web3, address=Address(self.arguments.first_token_address))
        self.second_token = ERC20Token(web3=self.web3, address=Address(self.arguments.second_token_address))

        self.token_first = Token(name=self.arguments.first_token_name,
                                 address=Address(self.arguments.first_token_address),
                                 decimals=self.arguments.first_token_decimals)

        self.token_second = Token(name=self.arguments.second_token_name,
                                  address=Address(self.arguments.second_token_address),
                                  decimals=self.arguments.second_token_decimals)

        self.min_eth_balance = Wad.from_number(self.arguments.min_eth_balance)

        self.gas_price = GasPriceFactory().create_gas_price(self.arguments)
        self.max_delta_on_percent = self.arguments.max_delta_on_percent

        self.price_feed = PriceFeedFactory().create_price_feed(self.arguments)

    def main(self):
        with Lifecycle(self.web3) as lifecycle:
            lifecycle.initial_delay(10)
            lifecycle.on_startup(self.startup)
            lifecycle.every(1, self.synchronize_price)

    def startup(self):
        self.approve()

    def approve(self):
        """Approve Uniswap to access our balances, so we can place orders."""
        self.uniswap_router.approve([self.first_token, self.second_token], directly(gas_price=self.gas_price))

    def our_available_balance(self, token: ERC20Token) -> Wad:
        if token.symbol() == self.token_first.name:
            return self.token_first.normalize_amount(token.balance_of(self.our_address))
        else:
            return self.token_second.normalize_amount(token.balance_of(self.our_address))

    @staticmethod
    def _get_amounts(market_price: Wad, first_token_liquidity_pool_amount: Wad,
                     second_token_liquidity_pool_amount: Wad):
        liquidity_pool_constant = first_token_liquidity_pool_amount * second_token_liquidity_pool_amount

        new_first_token_liquidity_pool_amount = sqrt(liquidity_pool_constant * market_price)
        new_second_token_liquidity_pool_amount = sqrt(liquidity_pool_constant / market_price)

        return AttrDict({
            'exact_value': first_token_liquidity_pool_amount - Wad.from_number(new_first_token_liquidity_pool_amount),
            'limit': Wad.from_number(new_second_token_liquidity_pool_amount) - second_token_liquidity_pool_amount,
        })

    def set_price(self, market_price: Wad, first_token: Address, second_token: Address,
                  max_delta_on_percent: int) -> Transact:
        pair = self.uniswap_router.get_pair(first_token=first_token, second_token=second_token)

        reserves = pair.reserves.map()

        uniswap_price = reserves[first_token] / reserves[second_token]
        delta = (market_price.value * 100 / uniswap_price.value) - 100

        self.logger.debug(f"market price = {market_price}")
        self.logger.debug(f"uniswap price = {uniswap_price}")
        self.logger.debug(f"the percentage difference between the market price and the uniswap price = {delta}")

        if delta > max_delta_on_percent:
            self.logger.debug("the price for uniswap is higher than the market price")
            input_data = self._get_amounts(market_price=market_price,
                                           first_token_liquidity_pool_amount=reserves[first_token],
                                           second_token_liquidity_pool_amount=reserves[second_token])

            calculate_amount = self.uniswap_router.get_amounts_out(amount_in=abs(input_data.exact_value),
                                                                   path=[first_token, second_token])
            calulate_price = abs(input_data.exact_value) / calculate_amount[-1]

            if abs(input_data.exact_value) > Wad.from_number(self.arguments.max_first_token_amount_input):
                self.logger.info(
                    f"Amount to send first_token > maximum allowed ({abs(input_data.exact_value)} > {self.arguments.max_first_token_amount_input})")
            elif abs(input_data.exact_value) > self.first_token.balance_of(self.our_address):
                self.logger.warning(f"There is not enough balance to change the price "
                                    f"(required: {abs(input_data.exact_value)}), "
                                    f"balance: {self.first_token.balance_of(self.our_address)}, "
                                    f"token={self.first_token.address.address}")
            elif calulate_price > market_price:
                self.logger.info(
                    f"new calulate price > market price ({calulate_price} > {market_price}). The price will not be changed")
            else:
                self.logger.info(
                    f"To change the price, you must perform an exchange ({abs(input_data.exact_value)} {first_token.address} -> {calculate_amount[-1]} {second_token.address})"
                )
                return self.uniswap_router.swap_from_exact_amount(amount_in=abs(input_data.exact_value),
                                                                  min_amount_out=calculate_amount[-1],
                                                                  path=[first_token, second_token])

        elif delta < 0 and abs(delta) > max_delta_on_percent:
            self.logger.debug("the market price is higher than the uniswap price")
            input_data = self._get_amounts(market_price=market_price,
                                           first_token_liquidity_pool_amount=reserves[first_token],
                                           second_token_liquidity_pool_amount=reserves[second_token])

            calculate_amount = self.uniswap_router.get_amounts_in(amount_out=abs(input_data.exact_value),
                                                                  path=[second_token, first_token])
            calulate_price = abs(input_data.exact_value) / calculate_amount[0]

            if calculate_amount[0] > Wad.from_number(self.arguments.max_second_token_amount_input):
                self.logger.info(
                    f"Amount to send second_token > maximum allowed ({calculate_amount[0]} > {self.arguments.max_second_token_amount_input})")
            elif calculate_amount[0] > self.second_token.balance_of(self.our_address):
                self.logger.warning(f"There is not enough balance to change the price "
                                    f"(required: {calculate_amount[0]}), "
                                    f"balance: {self.second_token.balance_of(self.our_address)}, "
                                    f"token={self.second_token.address.address}")
            elif calulate_price < market_price:
                self.logger.info(
                    f"new calulate price < market price ({calulate_price} < {market_price}). The price will not be changed")

            else:
                self.logger.info(
                    f"To change the price, you must perform an exchange ({calculate_amount[0]} {second_token.address} -> {abs(input_data.exact_value)} {first_token.address})"
                )
                return self.uniswap_router.swap_to_exact_amount(amount_out=abs(input_data.exact_value),
                                                                max_amount_in=calculate_amount[0],
                                                                path=[second_token, first_token])
        else:
            self.logger.debug("the price for uniswap satisfies the input accuracy. The price will not be changed")

    def synchronize_price(self):
        # market_maker = MarketMaker(self.uniswap_router)

        # If keeper balance is below `--min-eth-balance`, cancel all orders but do not terminate
        # the keeper, keep processing blocks as the moment the keeper gets a top-up it should
        # resume activity straight away, without the need to restart it.
        if eth_balance(self.web3, self.our_address) < self.min_eth_balance:
            self.logger.warning("Keeper ETH balance below minimum.")
            return

        if self.first_token.balance_of(self.our_address) < Wad.from_number(self.arguments.min_first_token_balance):
            self.logger.warning(f"Keeper {self.token_first.name} balance below minimum.")
            return

        if self.second_token.balance_of(self.our_address) < Wad.from_number(self.arguments.min_second_token_balance):
            self.logger.warning(f"Keeper {self.token_second.name} balance below minimum.")
            return

        target_price = self.price_feed.get_price()

        transaction = self.set_price(
            market_price=target_price.buy_price,
            first_token=self.first_token.address,
            second_token=self.second_token.address,
            max_delta_on_percent=self.max_delta_on_percent
        )

        if transaction is not None:
            transact = transaction.transact()
            if transact is not None and transact.successful:
                self.logger.info("The price was set successfully")


if __name__ == '__main__':
    UniswapV2MarketMakerKeeper(sys.argv[1:]).main()
