FROM ubuntu:20.10 AS base

WORKDIR /app/src/

RUN apt update -y && apt -y install clang-11 lldb-11 lld-11 && apt -y install clang && apt -y install util-linux

RUN apt update -y && apt -y install wget && apt -y install unzip && apt -y install make


RUN wget https://github.com/JBontes/CarlSAT_2021/archive/refs/heads/main.zip

RUN ls main.zip | xargs -n1 unzip
RUN rm main.zip


WORKDIR /app/src/CarlSAT_2021-main/
RUN make clean && make

### test ###
FROM mysql as DB


WORKDIR /app/

RUN apt update -y && apt -y install python3 && apt -y install python3-pip && apt -y install sudo

RUN pip3 install -U pymoo && pip3 install -U numpy && pip3 install -U mysql-connector-python 
ENV MYSQL_DATABASE hyperopt
ADD ./sqlscripts/ /docker-entrypoint-initdb.d/ 
COPY . .
EXPOSE 3306
