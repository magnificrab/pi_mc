FROM debian
LABEL maintainer="dgeorge@nycmail.com"
RUN apt-get update

RUN apt-get install -qq python3 python3-pip && \
	pip3 install --upgrade pip setuptools && \
	rm -r /root/.cache

RUN pip3 install requests==2.18.4

COPY pi_coord.py /usr/local/bin/pi_coord.py

CMD ["/usr/bin/python3", "/usr/local/bin/pi_coord.py"]
#CMD ["/bin/sh"]


