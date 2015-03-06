# This is a Dockerfile for running a SciPaas Container
# VERSION 1.0

FROM library/python:2

MAINTAINER Will Scott <willscott@gmail.com>

ADD . /scipaas/
WORKDIR /scipaas

RUN python sp init

EXPOSE 8081

ENTRYPOINT ["python", "sp", "go"]
