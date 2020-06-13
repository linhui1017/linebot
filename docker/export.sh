sudo docker save -o ubuntu_1604.tar ubuntu:16.04
sudo chown $USER:$USER ubuntu_1604.tar
sudo docker save -o flask_api.tar flask-api:latest
sudo chown $USER:$USER flask_api.tar