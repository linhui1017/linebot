# Oracle instant client
FROM ubuntu:18.04

MAINTAINER linhui <linhui@kfsyscc.org>


# Install Oracle
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev && \
    cd /usr/local/bin && \
    ln -s /usr/bin/python3 python && \
    pip3 install --upgrade pip && \
    apt-get install -y --no-install-recommends apt-utils && \
    apt-get install -y sqlite3 && \
    apt-get -y install alien libaio1 && \
    apt-get -y install locales locales-all && \
    mkdir -p /opt/app && \
    apt-get clean && rm -rf /var/cache/apt/* /var/lib/apt/lists/* /tmp/* /var/tmp/* 

# Locale 
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8

# Working Area
WORKDIR /opt/app
ADD ./app /opt/app

# Install Flask & GUNICON & SQLAlchemy
RUN apt-get update && \
    apt-get install -y && \
    pip install -r /opt/app/requirements.txt &&

ENV DOCKER_CONTAINER=1
EXPOSE 5000
EXPOSE 8000

# CMD specifcies the command to execute to start the server running.
CMD ["/opt/app/start.sh"]
# done
