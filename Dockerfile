FROM ubuntu:latest

RUN apt-get update
RUN apt-get upgrade
RUN apt-get install -y wget \
	vim \
	make \
	gcc \
	bc \
	cmake \
	python-pyasn1 \
	g++

# openssl build
RUN mkdir /app
WORKDIR /app
COPY ./dependencies/openssl-1.0.0.tar.gz /app/openssl-1.0.0.tar.gz

RUN tar -zxvf openssl-1.0.0.tar.gz
WORKDIR /app/openssl-1.0.0
RUN ./config
RUN make install
RUN ln -s /usr/local/ssl/bin/openssl /usr/local/sbin/openssl

# cado-nfs deps
WORKDIR /app
RUN apt-get install -y \
	python \
	python3 \
	git \
	libgmp3-dev

# cado-nfs build
COPY ./dependencies/cado-nfs-2.3.0.tar.gz /app/cado-nfs-2.3.0.tar.gz
RUN tar -zxvf cado-nfs-2.3.0.tar.gz
WORKDIR /app/cado-nfs-2.3.0
RUN cp local.sh.example local.sh
RUN echo 'build_tree="${up_path}/build/rsacrack"' >> local.sh
RUN make

WORKDIR /app
RUN apt-get install -y python-pip
RUN pip install requests bs4 lxml
COPY ./parser.py /app/parser.py
COPY ./rsa_reconstruction /app/rsa_reconstruction
COPY ./entrypoint.sh /app/entrypoint.sh

RUN chmod a+x parser.py
RUN chmod a+x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
