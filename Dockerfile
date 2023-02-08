FROM python:3.11-alpine
LABEL MAINTAINER="Lennart"

RUN apk add build-base git musl-dev libffi-dev openssl-dev jpeg-dev zlib-dev libwebp-dev


VOLUME /images

RUN mkdir -p /usr/src
WORKDIR /usr/src

COPY requirements.txt .
RUN pip install --compile --no-cache-dir git+https://github.com/lennart-k/mensa-utils
RUN pip install --compile --no-cache-dir -r requirements.txt

COPY . .

RUN pip install --compile --no-cache-dir --prefer-binary -e ./
RUN python -m compileall lunchbot

CMD [ "python", "-m", "lunchbot.server" ]
