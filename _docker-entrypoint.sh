#!/usr/bin/env bash

#cd "$(dirname "$0")"
#
#set -e

# The advantage of using this method, in contrary to just calling `pip3 install -r requirements.txt` several times,
# is that it can detect different versions of the same dependency and fail with a "Double requirement given"
# error message.
#pip install $(cat requirements.txt $(find lib -name requirements.txt | sort) | sort | uniq | sed 's/ *== */==/g')
#or
#pip install -r requirements.txt

#/app/bin/<%BIN_FILE%> <%PARAMS%>
/app/bin/oasis-market-maker-keeper


#cd /dir/to/mmk
#
#replace params
#
#docker-compose build && docker-compose up -d