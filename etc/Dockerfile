# This is a Dockerfile for running a SciPaas Container
# VERSION 1.0

FROM python:3.11-slim

MAINTAINER Will Scott <willscott@gmail.com>

ADD . /src/
WORKDIR /src

RUN python spc init

EXPOSE 8580

ENTRYPOINT ["python", "spc", "run"]
