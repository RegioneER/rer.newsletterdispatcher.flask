FROM python:3.8

WORKDIR /app

COPY . .

RUN apt-get update && \
    pip install -r requirements.txt && \
    buildout -N -c docker.cfg && \
    sed -i 's/bind 127.0.0.1 ::1/bind 0.0.0.0/g'  ./etc/redis.conf

EXPOSE 4000/tcp

ENTRYPOINT ["bin/supervisord", "-n"]
