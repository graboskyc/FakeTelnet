ENV PORT=22
FROM ubuntu
MAINTAINER graboskyc
ENV CONTAINER_SHELL=bash
ENV CONTAINER=

RUN apt-get update
RUN apt-get install -y git

RUN git clone https://github.com/graboskyc/FakeTelnet.git /opt/FakeTelnet

RUN useradd su -d /opt/FakeTelnet -M -s /opt/FakeTelnet/ciena.py
RUN echo wwp | passwd su --stdin
USER su
WORKDIR /opt/FakeTelnet

EXPOSE 22
