# Install Guide:

- Clone flask-api from gitlag.kfsyscc.org

  ```
  $git clone ssh://git@gitlab.kfsyscc.org:10022/deve/flask-api.git
  ```

- Install pip3 & virtualenv

  - Install pip first

  ```
  $sudo apt-get install python3-pip
  $sudo pip3 install virtualenv
  $virtualenv venv
  ```

- Install Redis-Server

  ```
  $sudo apt update
  $sudo apt install redis-server
  sudo systemctl restart redis.service
  ```

  ### Hint! Once you need force stop redis server:

  ```
  $cat /lib/systemd/system/redis-server.service
  $sudo mkdir /var/run/redis
  $sudo chown redis /var/run/redis
  $systemctl daemon-reload
  $systemctl stop redis-server
  ```

- Install Oracle Client

  ```
  $cd flask-api/docker
  $sudo ./instora.sh
  ```

- Modify start.sh

  - fixed: usr/bin/redis-server --> #user/bin/redis-server

  ```
  $vim start.sh
  ```

- Run flask-api

  ```
  $cd flask-api
  $source ./venv/bin/activate
  $(venv) .... /pip3 install -r requirements.txt
  $start.sh

  2019-04-02 08:18:16 [100454][info] Starting gunicorn 19.7.1
  2019-04-02 08:18:16 [100454][info] Listening at: http://0.0.0.0:5000 (100454)
  2019-04-02 08:18:16 [100454][info] Using worker: threads
  2019-04-02 08:18:16 [100454][info] Server is ready. Spawning workers
  2019-04-02 08:18:16 [100463][info] Booting worker with pid: 100463
  2019-04-02 08:18:16 [100464][info] Booting worker with pid: 100464
  2019-04-02 08:18:16 [100465][info] Booting worker with pid: 100465
  2019-04-02 08:18:16 [100466][info] Booting worker with pid: 100466
  ```

  - How to change sever IP?
    `$ vim gunicorn_config.py`

    - set "bind = os.getenv('GUNICORN\*BIND', '172.\*\*\*.\_\*\*.\_\_\_:5000')"

> 此專案特別超級感謝 輝哥大神 !!

### Appendix

- 每個 API 主要 Folder 下，建議放 index.py，參考程式碼如下:

```python
    from api.route import api_route
    from lib.utils import route_info

    @api_route(rule='', params=None, methods=['GET'])
    def index():
        return route_info('sys')
```
