# Base image
FROM python:3.9.15-alpine

# Install dependencies
RUN apk upgrade
RUN apk --update \
    add gcc \
    make \
    build-base \
    g++ \
    dumb-init 
    

# RUN rm /var/cache/apk/*

COPY . /tg-bot-harbor
WORKDIR /tg-bot-harbor
RUN pip3 install -r requirements.txt
RUN python3 /tg-bot-harbor/tg_secrets/setup.py build_ext --inplace
RUN rm -rf /tg-bot-harbor/tg_secrets
RUN rm -rf /tg-bot-harbor/build
RUN rm -r ~/.cache/pip

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

CMD ["sh", "-c", "gunicorn --workers=4 --threads=4 wsgi:app  -b 0.0.0.0:2233"]