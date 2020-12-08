FROM jenkins/jenkins:lts

USER root
ENV TZ=Europe/Moscow

RUN apt update
RUN apt install -y build-essential zlib1g-dev libncurses5-dev \
	libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev

RUN mkdir -p /opt/python38
RUN cd /opt/python38
RUN wget https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tar.xz
RUN tar -xf Python-3.8.2.tar.xz && cd Python-3.8.2 && ./configure --enable-optimizations && make altinstall

RUN rm -rf /opt/python38

RUN pip3.8 install --upgrade pip
RUN pip3.8 install pytest allure-pytest