#!/bin/bash
#/usr/bin/redis-server /opt/app/redis.conf
# Start Gunicorn processes
#pip install -r ./requirements.txt

echo Starting Gunicorn.
exec gunicorn app:app -c ./gunicorn_config.py --log-config ./gunicorn_logging.conf
 