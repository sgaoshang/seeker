# [launch]
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt ##(venv) $ pip freeze requirements.txt

(venv) $ export FLASK_APP=seeker.py

(venv) $ flask db init
(venv) $ flask db migrate
(venv) $ flask db upgrade

echo "export FLASK_APP=seeker.py" >> ~/.bash_profile

sqlite3 app.db < app/schema.sql

# [.env]
[debug mail]:
(venv) $ nohup python -u -m smtpd -n -c DebuggingServer localhost:8025 >> nohup.out 2>&1 &

# [random secret_key]
python -c "import uuid; print(uuid.uuid4().hex)"

# [deployment]
[updates]
(venv) $ git pull                              # download the new version
(venv) $ sudo supervisorctl stop seeker        # stop the current server
(venv) $ flask db upgrade                      # upgrade the database
(venv) $ flask translate compile               # upgrade the translations
(venv) $ sudo supervisorctl start seeker       # start a new server

rhel 7.4, server x86_64, minimal install

yum install python-pip mariadb-server postfix supervisor nginx git

[mariadb]
systemctl start mariadb
mysqladmin -u root -p password (default blank) (gaoshang)

$ mysql -p
mysql> create database seeker character set utf8 collate utf8_bin;
mysql> create user 'seeker'@'localhost' identified by '****<db-password>****';
mysql> grant all privileges on seeker.* to 'seeker'@'localhost';
mysql> flush privileges;
mysql> quit;

[requirements]
git clone https://github.com/sgaoshang/seeker.git
cd seeker/
pip install virtualenv
virtualenv venv
source venv/bin/activate
(venv) $ pip install -r requirements.txt

copy .env config file

[gunicorn]
(venv) $ pip install gunicorn pymysql
(venv) $ gunicorn -b localhost:8000 -w 4 seeker:app

[supervisord]
(venv) $ cat /etc/supervisord.d/seeker.ini
[program:seeker]
command=/root/seeker/venv/bin/gunicorn -b localhost:8000 -w 4 seeker:app
directory=/root/seeker
user=root
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true

(venv) $ supervisorctl start/stop seeker
(venv) $ supervisorctl reload
(venv) $ service supervisord stop
(venv) $ service supervisord start

systemctl enable supervisord.service
systemctl enable nginx.service
systemctl enable mariadb.service
systemctl disable firewalld.service
setenforce 0; vi /etc/selinux/config

Nginx:
$ mkdir certs
$ openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 -keyout certs/key.pem -out certs/cert.pem
Note: comment defaul server in /etc/nginx/nginx.conf
vi /etc/nginx/conf.d/seeker.conf see: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux
server {
    # listen on port 80 (http)
    listen 80;
    server_name _;
    location / {
        # redirect any requests to the same URL but on https
        return 301 https://$host$request_uri;
    }
}
server {
    # listen on port 443 (https)
    listen 443 ssl;
    server_name _;

    # location of the self-signed SSL certificate
    ssl_certificate /root/seeker/certs/cert.pem;
    ssl_certificate_key /root/seeker/certs/key.pem;

    # write access and error logs to /var/log
    access_log /var/log/seeker_access.log;
    error_log /var/log/seeker_error.log;

    location / {
        # forward application requests to the gunicorn server
        proxy_pass http://localhost:8000;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        # handle static files directly, without forwarding to the application
        alias /root/seeker/app/static;
        expires 30d;
    }
}
# when getting "connect() failed (111: Connection refused) while connecting to upstream, client .... fastcgi://[::1]:9000"
# use 127.0.0.1 instead of localhost, or remove the ipv6 alias from /etc/hosts

service nginx reload

setenforce 0
systemctl stop firewalld.service
systemctl disable firewalld.service
firewall-cmd --state (notrunning/running）

ipv6 issue:
$ ip -6 addr show
vi /etc/default/grub
edit GRUB_CMDLINE_LINUX="ipv6.disable=1"
grub2-mkconfig -o /boot/grub2/grub.cfg

*** server issue:
* upstream prematurely closed connection while reading response header from upstream
vi /etc/nginx/nginx.conf
  keepalive_timeout   600;