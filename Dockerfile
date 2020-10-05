FROM monolithos/setzer

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

COPY docker-entrypoint.sh /docker-entrypoint.sh


ENTRYPOINT ["/docker-entrypoint.sh"]