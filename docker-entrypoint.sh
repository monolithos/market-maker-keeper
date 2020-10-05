#!/bin/bash

deal_for=()

while [ "$1" != "" ]; do
    case $1 in
        --land )                  shift
                                  echo --------------------land--------------------
                                  export MARKET_MAKER_TYPE=land
                                  while [ "$1" != "" ]; do
                                      case $1 in
                                          -rpc | --rpc-host )                            shift
                                                                                  export RPC_HOST=$1
                                                                                         ;;

                                          -pk  | --address-private-key )                 shift
                                                                                  export ETH_PRIVATE_KEY=$1
                                                                                         ;;

                                          -a   | --eth-from )                            shift
                                                                                  export ETH_FROM=$1
                                                                                         ;;

                                          -m   | --market-address )                      shift
                                                                                  export MARKET_ADDRESS=$1
                                                                                         ;;

                                          -bta   | --buy-token-address )                 shift
                                                                                  export BUY_TOKEN_ADDRESS=$1
                                                                                         ;;

                                          -btn   | --buy-token-name )                    shift
                                                                                  export BUY_TOKEN_NAME=$1
                                                                                         ;;

                                          -btd   | --buy-token-decimals )                shift
                                                                                  export BUY_TOKEN_DECIMALS=$1
                                                                                         ;;

                                          -sta   | --sell-token-address )                 shift
                                                                                  export SELL_TOKEN_ADDRESS=$1
                                                                                         ;;

                                          -stn   | --sell-token-name )                    shift
                                                                                  export SELL_TOKEN_NAME=$1
                                                                                         ;;

                                          -std   | --sell-token-decimals )                shift
                                                                                  export SELL_TOKEN_DECIMALS=$1
                                                                                         ;;

                                          -b   | --bands )                               shift
                                                                                  export BANDS=$1
                                                                                         ;;

                                          -p   | --price-feed )                          shift
                                                                                  export PRICE_FEED=$1
                                                                                         ;;

                                          --price-feed-expiry )                          shift
                                                                                  export PRICE_FEED_EXPIRY=$1
                                                                                         ;;

                                          --round-places )                               shift
                                                                                  export ROUND_PLACES=$1
                                                                                         ;;

                                          --min-eth-balance )                            shift
                                                                                  export MIN_ETH_BALANCE=$1
                                                                                         ;;

                                          --rpc-timeout )                                shift
                                                                                  export RPC_TIMEOUT=$1
                                                                                         ;;

                                          --refresh-frequency )                          shift
                                                                                  export REFRESH_FREQUENCY=$1
                                                                                         ;;

                                          --market-support-address )                     shift
                                                                                  export MARKET_SUPPORT_ADDRESS=$1
                                                                                         ;;

                                          --ethgasstation-api-key )                      shift
                                                                                  export ETHGASSTATION_API_KEY=$1
                                                                                         ;;

                                          --fixed-gas-price )                            shift
                                                                                  export FIXED_GAS_PRICE=$1
                                                                                         ;;

                                          --price-offset )                               shift
                                                                                  export PRICE_OFFSET=$1
                                                                                         ;;

                                          * )                                            shift
                                                                                         ;;
                                      esac
                                                                                         shift
                                  done

                                  if [[ -z $ETH_PRIVATE_KEY || \
                                        -z $RPC_HOST || \
                                        -z $MARKET_ADDRESS || \
                                        -z $BUY_TOKEN_ADDRESS || \
                                        -z $BUY_TOKEN_NAME || \
                                        -z $BUY_TOKEN_DECIMALS || \
                                        -z $SELL_TOKEN_ADDRESS || \
                                        -z $SELL_TOKEN_NAME || \
                                        -z $SELL_TOKEN_DECIMALS || \
                                        -z $BANDS || \
                                        -z $PRICE_FEED || \
                                        -z $ETH_FROM ]] ;
                                  then
                                    cat docker-run-required-params.txt
                                    echo
                                    exit 1
                                  fi

                                  break
                              ;;

        --uniswap_v2 )                  shift
                                  echo --------------------uniswap_v2--------------------
                                  export MARKET_MAKER_TYPE=uniswap_v2
                                  while [ "$1" != "" ]; do
                                      case $1 in
                                          -rpc | --rpc-host )                            shift
                                                                                  export RPC_HOST=$1
                                                                                         ;;

                                          -pk  | --address-private-key )                 shift
                                                                                  export ETH_PRIVATE_KEY=$1
                                                                                         ;;

                                          -a   | --eth-from )                            shift
                                                                                  export ETH_FROM=$1
                                                                                         ;;

                                          -ra   | --router-address )                     shift
                                                                                  export ROUTER_ADDRESS=$1
                                                                                         ;;

                                          -fta   | --first-token-address )               shift
                                                                                  export FIRST_TOKEN_ADDRESS=$1
                                                                                         ;;

                                          -ftn   | --first-token-name )                  shift
                                                                                  export FIRST_TOKEN_NAME=$1
                                                                                         ;;

                                          -ftd   | --first-token-decimals )              shift
                                                                                  export FIRST_TOKEN_DECIMALS=$1
                                                                                         ;;

                                          -sta   | --second-token-address )              shift
                                                                                  export SECOND_TOKEN_ADDRESS=$1
                                                                                         ;;

                                          -stn   | --second-token-name )                 shift
                                                                                  export SECOND_TOKEN_NAME=$1
                                                                                         ;;

                                          -std   | --second-token-decimals )             shift
                                                                                  export SECOND_TOKEN_DECIMALS=$1
                                                                                         ;;

                                          -p   | --price-feed )                          shift
                                                                                  export PRICE_FEED=$1
                                                                                         ;;

                                          --price-feed-expiry )                          shift
                                                                                  export PRICE_FEED_EXPIRY=$1
                                                                                         ;;

                                          --max-delta-on-percent )                       shift
                                                                                  export MAX_DELTA_ON_PERCENT=$1
                                                                                         ;;

                                          --max-first-token-amount-input )               shift
                                                                                  export MAX_FIRST_TOKEN_INPUT=$1
                                                                                         ;;

                                          --max-second-token-amount-input )              shift
                                                                                  export MAX_SECOND_TOKEN_INPUT=$1
                                                                                         ;;

                                          --min-eth-balance )                            shift
                                                                                  export MIN_ETH_BALANCE=$1
                                                                                         ;;

                                          --min-first-token-balance )                    shift
                                                                                  export MIN_FIRST_TOKEN_BALANCE=$1
                                                                                         ;;

                                          --min-second-token-balance )                   shift
                                                                                  export MIN_SECOND_TOKEN_BALANCE=$1
                                                                                         ;;

                                          --rpc-timeout )                                shift
                                                                                  export RPC_TIMEOUT=$1
                                                                                         ;;

                                          --refresh-frequency )                          shift
                                                                                  export REFRESH_FREQUENCY=$1
                                                                                         ;;

                                          --ethgasstation-api-key )                      shift
                                                                                  export ETHGASSTATION_API_KEY=$1
                                                                                         ;;

                                          --fixed-gas-price )                            shift
                                                                                  export FIXED_GAS_PRICE=$1
                                                                                         ;;

#                                          --price-offset )                               shift
#                                                                                  export PRICE_OFFSET=$1
#                                                                                         ;;

                                          * )                                             shift
                                                                                          ;;
                                      esac
                                                                                          shift
                                  done

                                  if [[ -z $ETH_PRIVATE_KEY || \
                                        -z $RPC_HOST || \
                                        -z $ROUTER_ADDRESS || \
                                        -z $FIRST_TOKEN_ADDRESS || \
                                        -z $FIRST_TOKEN_NAME || \
                                        -z $FIRST_TOKEN_DECIMALS || \
                                        -z $SECOND_TOKEN_ADDRESS || \
                                        -z $SECOND_TOKEN_NAME || \
                                        -z $SECOND_TOKEN_DECIMALS || \
                                        -z $PRICE_FEED || \
                                        -z $ETH_FROM ]] ;
                                  then
                                    cat docker-run-required-params.txt
                                    echo
                                    exit 1
                                  fi
                                  break
                              ;;

        --mooniswap )                  shift
                                  echo --------------------mooniswap--------------------
                                  export MARKET_MAKER_TYPE=mooniswap
                        https://app.uniswap.org/          while [ "$1" != "" ]; do
                                      case $1 in
                                          -rpc | --rpc-host )                            shift
                                                                                  export RPC_HOST=$1
                                                                                         ;;

                                          -pk  | --address-private-key )                 shift
                                                                                  export ETH_PRIVATE_KEY=$1
                                                                                         ;;

                                          -a   | --eth-from )                            shift
                                                                                  export ETH_FROM=$1
                                                                                         ;;

                                          -fa   | --factory-address )                    shift
                                                                                  export FACTORY_ADDRESS=$1
                                                                                         ;;

                                          --referral-address )                           shift
                                                                                  export REFERRAL_ADDRESS=$1
                                                                                         ;;

                                          -fta   | --first-token-address )               shift
                                                                                  export FIRST_TOKEN_ADDRESS=$1
                                                                                         ;;

                                          -ftn   | --first-token-name )                  shift
                                                                                  export FIRST_TOKEN_NAME=$1
                                                                                         ;;

                                          -ftd   | --first-token-decimals )              shift
                                                                                  export FIRST_TOKEN_DECIMALS=$1
                                                                                         ;;

                                          -sta   | --second-token-address )              shift
                                                                                  export SECOND_TOKEN_ADDRESS=$1
                                                                                         ;;

                                          -stn   | --second-token-name )                 shift
                                                                                  export SECOND_TOKEN_NAME=$1
                                                                                         ;;

                                          -std   | --second-token-decimals )             shift
                                                                                  export SECOND_TOKEN_DECIMALS=$1
                                                                                         ;;

                                          -p   | --price-feed )                          shift
                                                                                  export PRICE_FEED=$1
                                                                                         ;;

                                          --price-feed-expiry )                          shift
                                                                                  export PRICE_FEED_EXPIRY=$1
                                                                                         ;;

                                          --max-delta-on-percent )                       shift
                                                                                  export MAX_DELTA_ON_PERCENT=$1
                                                                                         ;;

                                          --max-first-token-amount-input )               shift
                                                                                  export MAX_FIRST_TOKEN_INPUT=$1
                                                                                         ;;

                                          --max-second-token-amount-input )              shift
                                                                                  export MAX_SECOND_TOKEN_INPUT=$1
                                                                                         ;;

                                          --min-eth-balance )                            shift
                                                                                  export MIN_ETH_BALANCE=$1
                                                                                         ;;

                                          --min-first-token-balance )                    shift
                                                                                  export MIN_FIRST_TOKEN_BALANCE=$1
                                                                                         ;;

                                          --min-second-token-balance )                   shift
                                                                                  export MIN_SECOND_TOKEN_BALANCE=$1
                                                                                         ;;

                                          --rpc-timeout )                                shift
                                                                                  export RPC_TIMEOUT=$1
                                                                                         ;;

                                          --refresh-frequency )                          shift
                                                                                  export REFRESH_FREQUENCY=$1
                                                                                         ;;

                                          --ethgasstation-api-key )                      shift
                                                                                  export ETHGASSTATION_API_KEY=$1
                                                                                         ;;

                                          --fixed-gas-price )                            shift
                                                                                  export FIXED_GAS_PRICE=$1
                                                                                         ;;

#                                          --price-offset )                               shift
#                                                                                  export PRICE_OFFSET=$1
#                                                                                         ;;

                                          * )                                             shift
                                                                                          ;;
                                      esac
                                                                                          shift
                                  done

                                  if [[ -z $ETH_PRIVATE_KEY || \
                                        -z $RPC_HOST || \
                                        -z $FACTORY_ADDRESS || \
                                        -z $FIRST_TOKEN_ADDRESS || \
                                        -z $FIRST_TOKEN_NAME || \
                                        -z $FIRST_TOKEN_DECIMALS || \
                                        -z $SECOND_TOKEN_ADDRESS || \
                                        -z $SECOND_TOKEN_NAME || \
                                        -z $SECOND_TOKEN_DECIMALS || \
                                        -z $PRICE_FEED || \
                                        -z $ETH_FROM ]] ;
                                  then
                                    cat docker-run-required-params.txt
                                    echo
                                    exit 1
                                  fi
                                  break
                              ;;

        -h   | --help )           shift
                              cat docker-run-help-command.txt
                              echo
                              exit 1
                                  ;;

        --setzer-pairs )          shift
                              setzer pairs
                              echo
                              exit 1
                                  ;;

        * )                       shift
                                  ;;
    esac
                                  shift
done

if [[ -z $MARKET_MAKER_TYPE ]] ;
then
  echo 'Please specify market-maker'
  echo 'View the list of parameters `-h || --help`'
  echo
  exit 1
fi

python keeper.py