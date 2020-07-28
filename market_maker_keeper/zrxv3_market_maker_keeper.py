# This file is part of Maker Keeper Framework.
#
# Copyright (C) 2018 bargst
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

import sys
import time

from market_maker_keeper.zrx_market_maker_keeper import ZrxMarketMakerKeeper
from market_maker_keeper.band import NewOrder
from pyexchange.zrxv3 import ZrxApiV3, Pair
from pymaker import Address
from pymaker.zrxv3 import ZrxExchangeV3, ZrxRelayerApiV3


class ZrxV3MarketMakerKeeper(ZrxMarketMakerKeeper):
    """Keeper acting as a market maker on any 0x V3 exchange implementing the Standard 0x Relayer API V3."""

    def init_zrx(self):
        self.zrx_exchange = ZrxExchangeV3(web3=self.web3, address=Address(self.arguments.exchange_address))
        self.zrx_relayer_api = ZrxRelayerApiV3(exchange=self.zrx_exchange, api_server=self.arguments.relayer_api_server)
        self.zrx_api = ZrxApiV3(zrx_exchange=self.zrx_exchange, zrx_api=self.zrx_relayer_api)

        self.pair = Pair(sell_token_address=Address(self.arguments.sell_token_address),
                         sell_token_decimals=self.arguments.sell_token_decimals,
                         buy_token_address=Address(self.arguments.buy_token_address),
                         buy_token_decimals=self.arguments.buy_token_decimals)

    def place_order_function(self, new_order: NewOrder):
        assert(isinstance(new_order, NewOrder))

        order_expiry = int(new_order.band.params.get('orderExpiry', self.arguments.order_expiry))

        zrx_order = self.zrx_api.place_order(pair=self.pair,
                                             is_sell=new_order.is_sell,
                                             price=new_order.price,
                                             amount=new_order.amount,
                                             expiration=int(time.time()) + order_expiry)

        if zrx_order:
            if self.arguments.remember_own_orders:
                with self.placed_zrx_orders_lock:
                    self.placed_zrx_orders.append(zrx_order)

            order = self.zrx_api.get_orders(self.pair, [zrx_order])[0]

            return order

        else:
            return None


if __name__ == '__main__':
    ZrxV3MarketMakerKeeper(sys.argv[1:]).main()
