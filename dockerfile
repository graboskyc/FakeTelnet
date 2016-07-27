FROM 32bit/debian:jessie
MAINTAINER graboskyc
ENV PORT=22
ENV CONTAINER_SHELL=bash
ENV CONTAINER=

RUN apt-get clean && apt-get update && apt-get install -y git whois python2.7 openssh-server
RUN ln /usr/bin/python2.7 /usr/bin/python

#RUN yes | ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key
#RUN yes | ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key
RUN rm -r /etc/ssh/ssh*key
RUN dpkg-reconfigure openssh-server
#RUN mkdir /var/run/sshd
RUN echo 'root:screencast' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

RUN git clone https://github.com/graboskyc/FakeTelnet.git /opt/FakeTelnet
RUN chmod +x /opt/FakeTelnet/UserScripts/*

RUN useradd su -d /opt/FakeTelnet -M -s /opt/FakeTelnet/UserScripts/ciena.py -p `mkpasswd wwp`
USER su
WORKDIR /opt/FakeTelnet

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
