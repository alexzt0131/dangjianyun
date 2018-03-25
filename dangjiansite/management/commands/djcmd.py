import os, django
from dangjiansite.dangJianCmd import main
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dangjianyun.settings")
django.setup()
from dangjiansite.models import DjInfo



##################################settings##########################################
import logging

logging.basicConfig(level=logging.WARNING,
                    filename='./log/{}-log.txt'.format('djcmd'),
                    filemode='a',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')



#######################################已完成的################################################




###########################Django Command#################################################

from django.core.management.base import BaseCommand

class Command(BaseCommand): # 继承BaseCommand类，类名请保证为Command
    def handle(self, *args, **options): # 重写handle方法，该方法写入自定义命令要做的事（逻辑代码）

        djusers = [i for i in DjInfo.objects.all()]
        for i in djusers:
            print('*'*88)
            print('开始启动 {}'.format(i.djusername))
            print('*'*88)
            if i.iuser:
                main(i.iuser)



