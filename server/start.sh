#!/bin/sh

echo "curling"
#curl -XPUT -H 'Content-Type: application/json' 'http://shale:9200/_template/filebeat?pretty' -d@/etc/filebeat/filebeat.template.json
curl -XPUT -H 'Content-Type: application/json' 'http://rlyeh-a:9200/_template/filebeat?pretty' -d@/etc/filebeat/filebeat.template.json
echo "starting filebeat"
/etc/init.d/filebeat start  #compare to rc-service filebeat start
echo "starting circle_svc"
/usr/bin/python3 /usr/local/bin/circle_svc.py > /var/log/circle_svc.log 2>&1 &
echo "starting tail"
tail -f /var/log/circle_svc.log  #IS this necessary?
