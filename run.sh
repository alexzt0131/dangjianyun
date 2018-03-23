pkill -9 uwsgi
pkill -9 nginx
service nginx stop
cd /root/www/dangjianyun/
uwsgi3 --ini uwsgi.ini

service nginx start
#systemctl start nginx
