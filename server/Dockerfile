FROM debian
LABEL maintainer="dgeorge@nycmail.com"
RUN apt-get update

ENV FILEBEAT_VERSION 6.0.0

RUN apt-get install -qq python3 python3-pip && \
	pip3 install --upgrade pip setuptools && \
	rm -r /root/.cache

RUN pip3 install flask==0.12.2
RUN pip3 install structlog==17.2.0
RUN pip3 install autobahn==17.10.1
RUN pip3 install twisted==17.9.0
RUN pip3 install prometheus_client==0.0.21
RUN pip3 install gunicorn==19.7.1
#RUN pip3 install service_identity==17.0.0

COPY circle_svc.py /usr/local/bin/circle_svc.py

RUN apt-get install -qq curl

RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-${FILEBEAT_VERSION}-amd64.deb && \
	dpkg -i filebeat-${FILEBEAT_VERSION}-amd64.deb && \
	rm filebeat-${FILEBEAT_VERSION}-amd64.deb

COPY filebeat.template.json /etc/filebeat/filebeat.template.json

COPY filebeat.yml /etc/filebeat/filebeat.yml
RUN chmod 644 /etc/filebeat/filebeat.yml

RUN mkdir -p /etc/pki/tls/certs
COPY logstash-beats.crt /etc/pki/tls/certs/logstash-beats.crt

#COPY server.pem /usr/local/bin/server.pem
#RUN chmod 644 /usr/local/bin/server.pem

#TODO: debian cleanup
#RUN apk del --purge build-dependencies && \
#rm -rf /root/.cache /tmp/*

EXPOSE 5000

COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh
#CMD [ "/bin/sh" ]
CMD [ "/usr/local/bin/start.sh" ]
