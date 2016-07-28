FROM 32bit/debian:jessie
MAINTAINER graboskyc
ENV PORT=22
ENV CONTAINER_SHELL=bash
ENV CONTAINER=

RUN apt-get clean && apt-get update && apt-get install -y git whois python2.7 openssh-server
RUN ln /usr/bin/python2.7 /usr/bin/python

RUN rm -rf /etc/ssh/ssh*key
RUN dpkg-reconfigure openssh-server
RUN yes | ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key -N ""
RUN yes | ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N ""
#RUN chmod +r /etc/ssh/ssh*key

RUN git clone https://github.com/graboskyc/FakeTelnet.git /opt/FakeTelnet
RUN chmod +x /opt/FakeTelnet/UserScripts/*

RUN mv -f /opt/FakeTelnet/sshd_config /etc/ssh/
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

RUN service ssh start

RUN useradd su -d /opt/FakeTelnet -M -s /opt/FakeTelnet/UserScripts/ciena.py -p `mkpasswd wwp`
RUN useradd cisco -d /opt/FakeTelnet -M -s /opt/FakeTelnet/UserScripts/cisco.py -p `mkpasswd cisco`
RUN useradd juniper -d /opt/FakeTelnet -M -s /opt/FakeTelnet/UserScripts/juniper.py -p `mkpasswd juniper0`

CMD service ssh start;bash
EXPOSE 22
