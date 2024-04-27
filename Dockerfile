FROM python:3.8

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y vim && \
    pip install -r requirements.txt && \
    buildout -N -c docker.cfg
# sed -i 's/bind 127.0.0.1 ::1/bind 0.0.0.0/g'  ./etc/redis.conf

RUN chgrp -R 0 /app && chmod -R g=u /app

USER 1001

EXPOSE 4000/tcp

ENTRYPOINT ["bin/supervisord", "-n"]
