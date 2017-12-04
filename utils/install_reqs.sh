#!/bin/bash
  #attrs==17.3.0 \
  #Automat==0.6.0 \
  #certifi==2017.11.5 \
  #chardet==3.0.4 \
  #click==6.7 \
  #constantly==15.1.0 \
  #docopt==0.6.2 \
  #idna==2.6 \
  #incremental==17.5.0 \
  #itsdangerous==0.24 \
  #Jinja2==2.10 \
  #MarkupSafe==1.0 \
  #pipreqs==0.4.9 \
  #six==1.11.0 \
  #txaio==2.8.2 \
  #Werkzeug==0.12.2 \
  #yarg==0.1.9 \
  #zope.interface==4.4.3 

for pkg in \
  autobahn==17.10.1 \
  Flask==0.12.2 \
  hyperlink==17.3.1 \
  python3-prometheus-client==0.0.21 \
  requests==2.18.4 \
  structlog==17.2.0 \
  Twisted==17.9.0 \
  urllib3==1.22 
do
  pip install ${pkg/\=\=*.?/}
done
