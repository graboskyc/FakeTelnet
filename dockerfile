FROM 32bit/debian:jessie
MAINTAINER graboskyc
ENV PORT=22
ENV CONTAINER_SHELL=bash
ENV CONTAINER=

RUN apt-get update && apt-get install -y git whois python2.7

RUN git clone https://github.com/graboskyc/FakeTelnet.git /opt/FakeTelnet

RUN useradd su -d /opt/FakeTelnet -M -s /opt/FakeTelnet/UserScripts/ciena.py -p `mkpasswd wwp`
USER su
WORKDIR /opt/FakeTelnet

EXPOSE 22
