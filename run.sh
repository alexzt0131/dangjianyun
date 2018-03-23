pkill -9 uwsgi
pkill -9 nginx
cd /root/www/dangjianyun/
uwsgi3 --ini uwsgi.ini
systemctl start nginx
