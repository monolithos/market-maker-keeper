FROM python:3.6

#RUN groupadd -r maker && useradd --no-log-init -r -g maker maker

WORKDIR /app

#WORKDIR /opt/maker
#RUN chown -R maker /opt/maker
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY bin bin
#COPY lib /opt/maker/market-maker-keeper/lib
COPY market_maker_keeper market_maker_keeper
COPY docker-entrypoint.sh /docker-entrypoint.sh


#WORKDIR /opt/maker/market-maker-keeper

#USER maker

ENTRYPOINT ["/docker-entrypoint.sh"]