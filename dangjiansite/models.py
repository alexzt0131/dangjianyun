import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from dangjiansite.djfuncs import getFormedDateStr


class User(AbstractUser):     #继承AbstractUser
    desc = models.TextField()
    idjinfo = models.ForeignKey('DjInfo', null=True, blank=True,  verbose_name='党建信息')

    # models.OneToOneField
class DjInfo(models.Model):
    # device = models.ForeignKey('SIPDevice', null=True, blank=True, verbose_name='sipdevice')

    iuser = models.ForeignKey('User', null=True, blank=True, verbose_name='所属用户')
    djusername = models.CharField(max_length=50, verbose_name='党建云用户名')
    djpasswd = models.CharField(max_length=50, verbose_name='党建云密码')
    create_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.djusername




class DailyResult(models.Model):
    idjinfo = models.ForeignKey('DjInfo', null=True, blank=True, verbose_name='党建用户')
    create_date = models.DateTimeField(auto_now_add=True)
    create_day = models.CharField(max_length=50, verbose_name='创建日期', default=getFormedDateStr())
    thumb = models.CharField(max_length=50, verbose_name='信息评论')
    view = models.CharField(max_length=50, verbose_name='党员视角发布')
    hlep = models.CharField(max_length=50, verbose_name='互助广场回答')
    exam = models.CharField(max_length=50, verbose_name='在线知识竞答')
    study1 = models.CharField(max_length=50, verbose_name='在线阅读学习资料')
    study2 = models.CharField(max_length=50, verbose_name='学习资料写体会')
    conLogin = models.CharField(max_length=50, verbose_name='连续登录')
    mobileLogin = models.CharField(max_length=50, verbose_name='手机端登录')
    def __str__(self):
        return '{}:{}'.format(self.idjinfo, self.create_day)

class DailyDetail(models.Model):
    idjinfo = models.ForeignKey('DjInfo', null=True, blank=True, verbose_name='党建用户')
    create_date = models.DateTimeField(auto_now_add=True)
    create_day = models.CharField(max_length=50, verbose_name='创建日期', default=getFormedDateStr())
    thumbDetail = models.TextField(max_length=500, verbose_name='信息评论详细', default='')
    viewDetail = models.TextField(max_length=500, verbose_name='党员视角发布详细', default='')
    hlepDetail = models.TextField(max_length=500, verbose_name='互助广场回答详细', default='')
    examDetail = models.TextField(max_length=500, verbose_name='在线知识竞答详细', default='')
    study1Detail = models.TextField(max_length=500, verbose_name='在线阅读学习资料与学习资料写体会详细', default='')
    # study2Detail = models.TextField(max_length=500, verbose_name='学习资料写体会详细', default='')
    def __str__(self):
        return '（详细）{}:{}'.format(self.idjinfo, self.create_day)

# class DailyDetail(models.Model):
#     user = models.ForeignKey('User', null=True, blank=True,  verbose_name='用户')
#     create_date = models.DateTimeField(auto_now_add=True)
#     create_day = models.CharField(max_length=50, verbose_name='创建日期', default=getFormedDateStr())
#     thumbDetail = models.TextField(max_length=500, verbose_name='信息评论详细', default='')
#     viewDetail = models.TextField(max_length=500, verbose_name='党员视角发布详细', default='')
#     hlepDetail = models.TextField(max_length=500, verbose_name='互助广场回答详细', default='')
#     examDetail = models.TextField(max_length=500, verbose_name='在线知识竞答详细', default='')
#     study1Detail = models.TextField(max_length=500, verbose_name='在线阅读学习资料与学习资料写体会详细', default='')
#     # study2Detail = models.TextField(max_length=500, verbose_name='学习资料写体会详细', default='')
#     def __str__(self):
#         return '（详细）{}:{}'.format(self.user, self.create_day)
# class DailyResult(models.Model):
#     user = models.ForeignKey('User', null=True, blank=True,  verbose_name='用户')
#     create_date = models.DateTimeField(auto_now_add=True)
#     create_day = models.CharField(max_length=50, verbose_name='创建日期', default=getFormedDateStr())
#     thumb = models.CharField(max_length=50, verbose_name='信息评论')
#     view = models.CharField(max_length=50, verbose_name='党员视角发布')
#     hlep = models.CharField(max_length=50, verbose_name='互助广场回答')
#     exam = models.CharField(max_length=50, verbose_name='在线知识竞答')
#     study1 = models.CharField(max_length=50, verbose_name='在线阅读学习资料')
#     study2 = models.CharField(max_length=50, verbose_name='学习资料写体会')
#     conLogin = models.CharField(max_length=50, verbose_name='连续登录')
#     mobileLogin = models.CharField(max_length=50, verbose_name='手机端登录')
#     def __str__(self):
#         return '{}:{}'.format(self.user, self.create_day)
class ErrLog(models.Model):
    idjinfo = models.ForeignKey('DjInfo', null=True, blank=True, verbose_name='党建用户')
    create_day = models.CharField(max_length=50, verbose_name='创建日期', default=getFormedDateStr())
    content = models.TextField(max_length=1000, verbose_name='内容')
    def __str__(self):
        return '{}:{}\n{}'.format(self.idjinfo, self.create_day, self.content)


class ThumbLog(models.Model):
    # user = models.ForeignKey('User', null=True, blank=True, verbose_name='用户')
    idjinfo = models.ForeignKey('DjInfo', null=True, blank=True, verbose_name='党建用户')
    create_day = models.CharField(max_length=50, verbose_name='创建日期', default=getFormedDateStr())
    thumbId = models.TextField(max_length=500, verbose_name='评论id')
    def __str__(self):
        return '{}:{}\n{}'.format(self.idjinfo, self.create_day, self.thumbId)

class ExamInfo(models.Model):
    idjinfo = models.ForeignKey('DjInfo', null=True, blank=True, verbose_name='党建用户')
    create_day = models.CharField(max_length=50, verbose_name='创建日期', default=getFormedDateStr())
    create_time = models.CharField(max_length=50, verbose_name='创建时间', default=datetime.datetime.now().strftime("%H:%M:%S"))
    question = models.TextField(max_length=500, verbose_name='问题')
    answer = models.CharField(max_length=50, verbose_name='答案')
    answerText = models.CharField(max_length=50, verbose_name='文本答案')
    def __str__(self):
        return '{}:{}\n{}'.format(self.idjinfo, self.create_day, self.question)

class ExamDetail(models.Model):
    idjinfo = models.ForeignKey('DjInfo', null=True, blank=True, verbose_name='党建用户')
    create_day = models.CharField(max_length=50, verbose_name='创建日期', default=getFormedDateStr())
    subjectId = models.CharField(max_length=50, verbose_name='题目id')
    title = models.CharField(max_length=500, verbose_name='题目名称')
    detail = models.TextField(max_length=500, verbose_name='详细')
    def __str__(self):
        return '{}:{}\n{}'.format(self.idjinfo, self.create_day, self.title)

class Qa(models.Model):
    question = models.TextField(max_length=500, verbose_name='问题')
    answer = models.CharField(max_length=50, verbose_name='答案')
    answerText = models.CharField(max_length=50, verbose_name='文本答案')
    def __str__(self):
        return '{}:{}\n{}'.format(self.question, self.answerText, self.answer)

class StudyInfo(models.Model):
    idjinfo = models.ForeignKey('DjInfo', null=True, blank=True, verbose_name='党建用户')
    create_day = models.CharField(max_length=50, verbose_name='创建日期', default=getFormedDateStr())
    create_time = models.CharField(max_length=50, verbose_name='创建时间', default=datetime.datetime.now().strftime("%H:%M:%S"))
    reply = models.TextField(max_length=500, verbose_name='回复内容')
    title = models.CharField(max_length=150, verbose_name='标题')
    def __str__(self):
        return '{}:{}\n{}'.format(self.idjinfo, self.create_day, self.title)

class HelpInfo(models.Model):
    idjinfo = models.ForeignKey('DjInfo', null=True, blank=True, verbose_name='党建用户')
    create_day = models.CharField(max_length=50, verbose_name='创建日期', default=getFormedDateStr())
    create_time = models.CharField(max_length=50, verbose_name='创建时间', default=datetime.datetime.now().strftime("%H:%M:%S"))
    reply = models.TextField(max_length=500, verbose_name='回复内容')
    title = models.CharField(max_length=50, verbose_name='标题')
    def __str__(self):
        return '{}:{}\n{}'.format(self.idjinfo, self.create_day, self.title)

class ViewInfo(models.Model):
    idjinfo = models.ForeignKey('DjInfo', null=True, blank=True, verbose_name='党建用户')
    create_day = models.CharField(max_length=50, verbose_name='创建日期', default=getFormedDateStr())
    create_time = models.CharField(max_length=50, verbose_name='创建时间',
                                   default=datetime.datetime.now().strftime("%H:%M:%S"))
    pub_content = models.TextField(max_length=500, verbose_name='发布内容')


    def __str__(self):
        return '{}:{}\n{}'.format(self.idjinfo, self.create_day, self.pub_content)

class ThumbInfo(models.Model):
    idjinfo = models.ForeignKey('DjInfo', null=True, blank=True, verbose_name='党建用户')
    create_day = models.CharField(max_length=50, verbose_name='创建日期', default=getFormedDateStr())
    create_time = models.CharField(max_length=50, verbose_name='创建时间',
                                   default=datetime.datetime.now().strftime("%H:%M:%S"))
    reply = models.TextField(max_length=500, verbose_name='回复内容')
    title = models.CharField(max_length=150, verbose_name='标题')
    def __str__(self):
        return '{}:{}\n{}'.format(self.idjinfo, self.create_day, self.title)
