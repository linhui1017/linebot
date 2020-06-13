docker stop flask-api
docker rm flask-api
docker run -d --name flask-api \
  --env HIS_ORA=TEST \
  -v /etc/localtime:/etc/localtime:ro \
  --dns 172.16.254.51 --dns 8.8.8.8 \
  -v /home/neo/flask-api:/opt/app \
  -p 5000:5000 \
  --restart=unless-stopped \
  -t "flask-api"

