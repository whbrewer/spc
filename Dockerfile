# This is a Dockerfile for running a SciPaas Container
# VERSION 1.0

FROM library/python:2

MAINTAINER Will Scott <willscott@gmail.com>

ADD . /sciplex/
WORKDIR /sciplex

RUN python spx init

EXPOSE 8580

ENTRYPOINT ["python", "spx", "go"]
