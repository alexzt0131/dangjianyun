cd /root/www/dangjianyun/
python3 manage.py djcmd
mysqldump -uroot -pApasswd myproject > /root/dbbackup/`date+%y%m%d`.sql

find /root/dbbackup/ f -mtime +7 -exec rm {}\; 
