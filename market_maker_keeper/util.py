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
import json
import logging

import re

from telegram_log_handler import TelegramHandler


def setup_logging(arguments):
    # telegram_handler = get_telegram_handler(arguments)
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s',
                        level=(logging.DEBUG if arguments.debug else logging.INFO))
    logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.INFO)


def get_telegram_handler(arguments):
    with open(arguments.telegram_log_config_file, 'r') as f:
        telegram_log = json.loads(f.read())

    telegram_handler = TelegramHandler(
        bot_token=telegram_log['bot_token'],
        chat_ids=telegram_log['chat_ids'],
        project_name=telegram_log['project_name'],
        use_proxy=telegram_log['use_proxy'],
        request_kwargs=telegram_log['request_kwargs']

    )

    telegram_handler.setLevel(logging.WARNING)

    return telegram_handler
    # self.logger.addHandler(telegram_handler)


def sanitize_url(url):
    return re.sub("://([^:@]+):([^:@]+)@", "://\g<1>@", url)
