FROM monolithos/setzer

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

COPY _docker-entrypoint.sh /docker-entrypoint.sh


ENTRYPOINT ["/docker-entrypoint.sh"]