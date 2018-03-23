import base64
import csv
import datetime
import random
import re
import time

import os
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from dangjiansite.models import User, DjInfo, DailyResult, DailyDetail, ErrLog, ThumbLog, ThumbInfo, StudyInfo, \
    HelpInfo, ViewInfo, ExamInfo
from dangjianyun import settings
from dangjiansite.djfuncs import decodeStr, getFormedDateStr, checkScore
from dangjiansite.runner import Runner
import logging

logging.basicConfig(level=logging.WARNING,
                    filename='./log/{}-log.txt'.format('view'),
                    filemode='a',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
###########################################################################
#测试区
def testt(request):

    viewPublic(request, run=Runner(username='024549', password='Aa1234'))


############################################################################
# 党建云执行函数

# 暂时可用，有待优化循环中的代码，再看看还有什么问题
def thumbTen(request, run):
    '''
    判断执行次数操作，并将结果写入文件
    :param run:
    :return:
    '''
    loginUser = request.user.username
    loginUserObj = None
    try:
        loginUserObj = User.objects.get(username=loginUser)
    except Exception as e:
        print(e)
        logging.exception("msg: {}.".format(str(e)))
    thumbTimes = run.getExcuteTimes()['thumb']
    current = checkScore(run)['thumb'].split('/')[0]
    total = checkScore(run)['thumb'].split('/')[1]
    # print(current, total)
    # if thumbTimes == 0:
    print('@' * 88)
    print('需点赞：', thumbTimes)
    if current == total:
        print('无需点赞操作')
        thumbTimes = 0
    for i in range(thumbTimes):
        print('还有{}个页面可选。'.format(len(run.thumbPages)))
        print('debug out put.', run.thumbPages)
        print('已经点赞{}个'.format(len(run.thumbedPages) + 1))
        id = random.choice(run.thumbPages)
        thumbedSet = []
        thumbedSet.extend(run.thumbedPages)
        thumbedSet.extend(run.multiThumbed)
        thumbedSet.extend(run.thumbedFileList)
        thumbedId = [i.thumbId for i in ThumbLog.objects.filter(user=loginUserObj)]  # 数据多了会造成负担，需要想办法不要每次循环都这么做
        if id not in thumbedSet and id not in thumbedId:
            detail = run.doThumb(id=id)
            ThumbLog.objects.create(
                user=loginUserObj,
                thumbId=id,
            ).save()
            time.sleep(16)
            dobj = getDailyDetailObj(request)
            try:
                dobj.thumbDetail += '{}<br/>'.format(detail)
            except Exception as e:
                dobj.thumbDetail = ''
                pass
            text = dobj.thumbDetail
            pat = r'<br/>'
            s = re.compile(pat).sub('', text)
            dobj.thumbDetail = s
            dobj.save()

        else:
            print('id {} 已经赞过。'.format(id))


# 完成 已重构
def study(request, run):
    '''
    判断执行次数操作，并将结果写入文件
    :param run:
    :return:
    '''
    studyTimes = run.getExcuteTimes()['study']
    current1 = checkScore(run)['study1'].split('/')[0]
    total1 = checkScore(run)['study1'].split('/')[1]
    current2 = checkScore(run)['study2'].split('/')[0]
    total2 = checkScore(run)['study2'].split('/')[1]

    if current1 == total1 and current2 == total2:
        print('无需学习操作')
        studyTimes = 0  # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    for i in range(studyTimes):
        print('还有{}个页面可选。'.format(len(run.studyPages)))
        print('debug out put.', run.studyPages)
        mid = random.choice(run.studyPages)
        # 记录访问的标题与id
        for i in run.studyPageList:
            if mid == i[1]:
                run.studyRsults.update({'title': i[0]})
        run.doStudy(mid=mid)
    # 写入当日result文件
    if run.studyRsults:
        result = "学习主题: {}\n回复内容：\n{}\n".format(run.studyRsults['title'], run.studyRsults['content'])
        print(result)
        dobj = getDailyDetailObj(request)
        try:
            dobj.study1Detail += '{}<br/>'.format(result)
        except Exception as e:
            dobj.study1Detail = ''
            pass
        text = dobj.study1Detail
        pat = r'<br/>'
        s = re.compile(pat).sub('', text)
        dobj.study1Detail = s
        dobj.save()
        write2File(run, './results/', 'result.txt', result)


# 完成 已重构
def viewPublic(request, run):
    '''
    发布党员视野
    :param run:
    :return:
    '''
    viewTimes = run.getExcuteTimes()['view']
    current = checkScore(run)['view'].split('/')[0]
    total = checkScore(run)['view'].split('/')[1]
    if current == total:
        print('无需党员视野发布操作')
        viewTimes = 0
    for i in range(viewTimes):
        print('已经发布{}个'.format(len(run.viewsResults)))
        detail = run.doView()
        # print(detail)
        dobj = getDailyDetailObj(request)
        try:
            dobj.viewDetail += '{}<br/>'.format(detail)
        except Exception as e:
            dobj.viewDetail = ''
            pass
        text = dobj.viewDetail
        pat = r'<br/>'
        s = re.compile(pat).sub('', text)
        dobj.viewDetail = s
        dobj.save()


# 完成 已重构
def help(request, run):
    '''
    互助模块
    将结果写入文件
    :param run:
    :return:
    '''
    helpTimes = run.getExcuteTimes()['help']
    current = checkScore(run)['help'].split('/')[0]
    total = checkScore(run)['help'].split('/')[1]
    if current == total:
        print('无需互助操作')
        helpTimes = 0
    for i in range(helpTimes):
        print('还有{}个页面可选。'.format(len(run.helpPages)))
        print('debug out put.', run.helpPages)
        print('已经互助{}个'.format(len(run.helpedPages)))
        id = random.choice(run.helpPages)
        if id not in run.helpedPages:
            detail, log = run.doHelp(id=id)  # log暂时不知用不用

            dobj = getDailyDetailObj(request)
            try:
                dobj.hlepDetail += '{}<br/>'.format(detail)
            except Exception as e:
                dobj.hlepDetail = ''
                pass
            text = dobj.hlepDetail
            pat = r'<br/>'
            s = re.compile(pat).sub('', text)
            dobj.hlepDetail = s
            dobj.save()


###做测试用
@csrf_exempt
def adduser1(request):
    ###做测试用
    # adduser(request)

    loginUser = request.user.username
    loginUserObj = None
    ret = {
        'scores': None,
        'userinfo': None,
        'retmsg': '',
        'dailyInfo': None,
        'dailyDetail': None,
    }
    dailyInfo = None
    try:
        print('in try')
        loginUserObj = User.objects.get(username=loginUser)
        print(loginUserObj.username)
        print(loginUserObj.idjinfo)
    except Exception as e:
        print(e)

    username = loginUserObj.idjinfo.djusername
    passwd = decodeStr(loginUserObj.idjinfo.djpasswd)
    print(username, passwd)
    run = Runner(username=username, password=passwd)
    # try:
    thumbTen(request=request, run=run)
    # viewPublic(request=request, run=run)

    return render(request, 'index.html')


######################################
# backup


# def thumbTen(request, run):
#     '''
#     判断执行次数操作，并将结果写入文件
#     :param run:
#     :return:
#     '''
#     thumbTimes = run.getExcuteTimes()['thumb']
#     current = checkScore(run)['thumb'].split('/')[0]
#     total = checkScore(run)['thumb'].split('/')[1]
#     # print(current, total)
#     # if thumbTimes == 0:
#     if current == total:
#         print('无需点赞操作')
#         thumbTimes = 0
#     for i in range(thumbTimes):
#         print('还有{}个页面可选。'.format(len(run.thumbPages)))
#         print('debug out put.', run.thumbPages)
#         print('已经点赞{}个'.format(len(run.thumbedPages) + 1))
#         id = random.choice(run.thumbPages)
#         thumbedSet = []
#         thumbedSet.extend(run.thumbedPages)
#         thumbedSet.extend(run.multiThumbed)
#         thumbedSet.extend(run.thumbedFileList)
#         if id not in thumbedSet:
#             detail = run.doThumb(id=id)
#             time.sleep(16)
#             dobj = getDailyDetailObj(request)
#             try:
#                 dobj.thumbDetail += '{}<br/>'.format(detail)
#             except Exception as e:
#                 dobj.thumbDetail = ''
#                 pass
#             text = dobj.thumbDetail
#             pat = r'<br/>'
#             s = re.compile(pat).sub('', text)
#             dobj.thumbDetail = s
#             dobj.save()
#
#         else:
#             print('id {} 已经赞过。'.format(id))


# dobj = getDailyDetailObj(request)
#    print('*' * 88)
#    print(detail)
#    print(dobj)
#    objField = None
#    if field == 'help':
#        objField =
#    try:
#        dobj.hlepDetail += '{}<br/>'.format(detail)
#    except Exception as e:
#        dobj.hlepDetail = ''
#        pass
#    text = dobj.hlepDetail
#    pat = r'<br/>'
#    s = re.compile(pat).sub('', text)
#    print(s)
#    dobj.hlepDetail = s
#    dobj.save()

# def help(run, request):
#     '''
#     互助模块
#     将结果写入文件
#     :param run:
#     :return:
#     '''
#     helpTimes = run.getExcuteTimes()['help']
#     current = checkScore(run)['help'].split('/')[0]
#     total = checkScore(run)['help'].split('/')[1]
#     if current == total:
#         print('无需互助操作')
#         helpTimes = 0
#     for i in range(helpTimes):
#         print('还有{}个页面可选。'.format(len(run.helpPages)))
#         print('debug out put.', run.helpPages)
#         print('已经互助{}个'.format(len(run.helpedPages)))
#         id = random.choice(run.helpPages)
#         if id not in run.helpedPages:
#             run.doHelp(id=id, callback=w2db)


#######################################


def checkScore(run):
    '''
    次函数用来获得用户的今日得分
    :param run:
    :return:
    '''
    credInfo = run.getCredItinfo()
    ret = {
        'thumb': credInfo[1]['信息评论'],
        'exam': credInfo[1]['在线知识竞答'],
        'view': credInfo[1]['党员视角发布'],
        'help': credInfo[1]['互助广场回答'],
        'study1': credInfo[1]['在线阅读学习资料'],
        'study2': credInfo[1]['学习资料写体会'],
    }
    return ret


def write2File(run, path, filename, content):
    if not path.endswith('/'):
        filename = '/' + filename
    fullPath = '{}{}-{}{}'.format(path, run.currentTime[0: 8], run.username, filename)
    if not os.path.exists(path):
        os.mkdir(path)
    with open(fullPath, 'a') as f:
        f.write('{}-{}\n'.format(run.currentTime, content))
    print('内容已经写入{}'.format(fullPath))


def getAnswersFromFile():
    answers = []
    filePath = './answers/new19.csv'
    with open(filePath, 'r', encoding='utf8') as f:
        # print(f.readlines())
        csvReader = csv.reader(f)
        for i in csvReader:
            answers.append((i[0], i[1], i[2]))
        return answers


def getAnswer(question):
    data = getAnswersFromFile()
    # print(data)
    for i in data:
        if question == i[0]:
            return i


# def exam(run):
#     examTimes = run.getExcuteTimes()['exam']
#     current = checkScore(run)['exam'].split('/')[0]
#     total = checkScore(run)['exam'].split('/')[1]
#     print(current, total)
#     print(examTimes)
#     if current == total:
#         print('无需做题操作')
#     # for i in range(examTimes):
#     run.doExam()  # 次函数有问题500 失败


def encodeStr(str):
    return base64.b64encode(bytes(str, encoding='utf8'))


def decodeStr(bytes):
    return base64.b64decode(bytes).decode('utf8')


def getFormedDateStr():
    return datetime.datetime.now().strftime("%Y-%m-%d")


###################################################################################
# 页面使用的方法







#已重构
def getDailyDetailObj(request):
    '''
    返回一个当日dailydetail对象，没有就创建一个返回
    :param request:
    :return:
    '''
    loginUser = request.user.username
    loginUserObj = None
    try:
        loginUserObj = User.objects.get(username=loginUser)
    except Exception as e:
        print(e)
    today = getFormedDateStr()

    dobj = DailyDetail.objects.filter(create_day=today).filter(idjinfo=loginUserObj.idjinfo)
    # print('777777777'*11)
    # print(dobj)
    # print(dobj[0])
    # print('777777777' * 11)
    if not dobj:
        DailyDetail.objects.create(idjinfo=loginUserObj.idjinfo).save()
        return DailyDetail.objects.filter(create_day=today).filter(idjinfo=loginUserObj.idjinfo)[0]
    else:
        return dobj[0]


# 暂时可用，待检查
@csrf_exempt
def do_login(request):
    # adduser(request)
    login_user = request.user.username
    ret = {
        'title': '登录',
        'login_user': login_user,
        'error': '',
    }

    lf = LogForm()
    ret['lf'] = lf

    if request.method == 'POST':
        checkForm = LogForm(request.POST)
        if checkForm.is_valid():
            print('a')
            print(checkForm.cleaned_data['username'], checkForm.cleaned_data['password'])
            try:
                user = User.objects.get(username=checkForm.cleaned_data['username'])
                if user.check_password(checkForm.cleaned_data['password']):
                    print('passwd:{}'.format(checkForm.cleaned_data['password']))
                    login(request, user)
                    print('在这跳转的')
                    return HttpResponseRedirect('/index/')

                else:
                    ret['error'] = '帐号或密码错误，请重新输入。'
                    ret['lf'] = checkForm

            except Exception as e:
                print(e)
                ret['error'] = '帐号或密码错误，请重新输入。'
                ret['lf'] = checkForm

        else:
            errobj = checkForm.errors
            print(type(errobj))
            es = checkForm.errors.as_json()
            print(type(es))
            err = es.split('"')[-2]
            print(err)
            ret['error'] = err
            ret['lf'] = checkForm

    return render(request, 'login.html', ret)


# 定义检测登录的装饰器
def check_login(func):
    def wrapper(request, *args, **kwargs):
        # print('in wrapper')
        if request.user.is_authenticated():
            # return HttpResponseRedirect('/login/')
            # print('shi')
            return func(request, *args, **kwargs)
        else:
            # print('fou')
            return redirect('/login/')

    return wrapper


def adduser(request):
    username = '4549'
    password = 'Aa123456'
    User.objects.create(password=make_password(password),
                            username=username)
    username = '3592'
    password = 'Aa123456'
    User.objects.create(password=make_password(password),
                            username=username)
    username = '4040'
    password = 'Aa123456'
    User.objects.create(password=make_password(password),
                            username=username)
#     try:
#         flag = User.objects.get(username=username)
#         return HttpResponse("<script>alert('用户已存在');window.location.href='/login/';</script>")

#     except Exception as e:
#         User.objects.create(password=make_password(password),
#                             username=username)
#     return HttpResponse("<script>alert('成功');window.location.href='/login';</script>")
    pass


def do_logout(request):
    print('in logout')
    try:
        if request.user.is_authenticated():
            print('in logout try')
            logout(request)
            return HttpResponseRedirect('/index/')
        else:
            return HttpResponse("<script>alert('你还没有登录');window.history.back(-1);</script>")
    except Exception as e:
        print(e)
        return HttpResponseRedirect('/index/')


# 此函数用来提供给模板中直接调用settings中的全局变量
# def global_settings(request):
#     '''
#     此函数用来提供给模板中直接调用settings中的全局变量
#     需要在settings TEMPLATES 中添加此函数
#     'security.views.global_settings',
#     :param request:
#     :return:
#     '''
#     return {
#         'CONTACT_TEL': settings.CONTACT_TEL,
#     }


#################################################################################################
# 页面函数
def getBindedUser(userObj):
    try:
        return userObj.idjinfo.djusername
    except Exception as e:
        print(e)
        return None
@csrf_exempt
def config(request):
    loginUser = request.user.username
    loginUserObj = None
    try:
        loginUserObj = User.objects.get(username=loginUser)
    except Exception as e:
        print(e)


    ret = {
        'retmsg': '',
        'loginUser': loginUser,
        'bindUser': getBindedUser(loginUserObj),
    }

    if request.method == 'POST':

        djusername = request.POST.get('username')
        djpasswd = request.POST.get('passwd')

        encodedPasswd = encodeStr(djpasswd)
        try:
            djobj = DjInfo.objects.get(djusername=djusername)
            print('存在djboj')
            #
            if not djobj.iuser:
                print('in here')
                loginUserObj.idjinfo = djobj
                loginUserObj.save()
                djobj.iuser = loginUserObj
                djobj.save()
                ret['retmsg'] = '设置成功1'

            else:
                if loginUserObj.idjinfo and loginUserObj.idjinfo.djusername == djobj.djusername:
                    djobj.djpasswd = encodedPasswd
                    djobj.save()
                    ret['retmsg'] = '用户存在,只修改密码。'
                else:
                    ret['retmsg'] = '{}已被绑定。'.format(djusername)
        except Exception as e:
            if not loginUserObj.idjinfo:  # 登录用户没有idjinfo的时候才创建
                if Runner(username=djusername, password=decodeStr(encodedPasswd)).getToken():
                    DjInfo.objects.create(
                        iuser=loginUserObj,
                        djusername=djusername,
                        djpasswd=encodedPasswd).save()
                    djobj = DjInfo.objects.get(djusername=djusername)
                    loginUserObj.idjinfo = djobj
                    loginUserObj.save()
                    ret['retmsg'] = '设置成功'
                else:
                    ret['retmsg'] = '获得token失败，请确认帐号与密码正确后重试。'
        # try:
        #     djobj = DjInfo.objects.get(djusername=djusername)
        #     if loginUserObj.idjinfo and loginUserObj.idjinfo.djusername == djobj.djusername:
        #         djobj.djpasswd = encodedPasswd
        #         djobj.save()
        #         ret['retmsg'] = '用户存在,只修改密码。'
        #     else:
        #         ret['retmsg'] = '该党建云帐号已被绑定。'
        #         pass
        #
        # except Exception as e:
        #     if not loginUserObj.idjinfo:  # 登录用户没有idjinfo的时候才创建
        #         if Runner(username=djusername, password=decodeStr(encodedPasswd)).getToken():
        #             DjInfo.objects.create(
        #                 iuser=loginUserObj,
        #                 djusername=djusername,
        #                 djpasswd=encodedPasswd).save()
        #             djobj = DjInfo.objects.get(djusername=djusername)
        #             loginUserObj.idjinfo = djobj
        #             loginUserObj.save()
        #             ret['retmsg'] = '设置成功'
        #         else:
        #             ret['retmsg'] = '获得token失败，请确认帐号与密码正确后重试。'
        #     else:
        #         ret['retmsg'] = '当前用户已绑定帐号{}'.format(loginUserObj.idjinfo.djusername)

        # 待记录到mysql，按照此参数执行
    ret['bindUser'] = getBindedUser(loginUserObj)
    return render(request, 'config.html', ret)



@csrf_exempt
def functions(request):
    loginUser = request.user.username
    loginUserObj = None
    ret = {
        'retmsg': '',
        'loginUser': loginUser,
    }
    dailyInfo = None
    try:
        loginUserObj = User.objects.get(username=loginUser)
    except Exception as e:
        print(e)

    if request.method == 'GET':
        print(request.GET)
        act = request.GET.get('act', None)
        if act:
            if act == 'unbind':
                # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                oldBind = loginUserObj.idjinfo.djusername
                loginUserObj.idjinfo = None
                loginUserObj.save()
                djobj = DjInfo.objects.get(djusername=oldBind)
                djobj.iuser = None
                djobj.save()
                ret['bindUser'] = getBindedUser(loginUserObj)
                # djobj.delete()#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<暂时先不删除mark

                ret['retmsg'] = '已与{}解除绑定。'.format(oldBind)
                # 这里需要改成弹出窗口
                return render(request, 'config.html', ret)
                # return HttpResponseRedirect('/index/')
        else:
            return HttpResponse("<h1>无效的访问</h1>")

    return render(request, 'index.html', ret)


@csrf_exempt
def info(request):
    loginUser = request.user.username
    loginUserObj = None
    ret = {
        'loginUser': loginUser,
        'scores': None,
        'userinfo': None,
        'retmsg': '',
        'dailyInfo': None,
        'dailyDetail': None,
    }
    dailyInfo = None
    try:
        loginUserObj = User.objects.get(username=loginUser)
    except Exception as e:
        print(e)
    try:
        dailyInfo = DailyResult.objects.filter(idjinfo=loginUserObj.idjinfo).order_by('-create_date')
    except Exception as e:
        print(e)
    try:
        dailyDetail = DailyDetail.objects.filter(idjinfo=loginUserObj.idjinfo)
    except Exception as e:
        print(e)

    # print(dailyInfo)
    # print(type(dailyInfo))
    print(dailyDetail)
    print('8'*88)
    print(dailyInfo)
    '''
    次函数应该是反映当天完成的情况记录，应该从数据库中先看有无数据
    :param request:
    :return:
    '''
    # 待改为ajax 以提高用户体验
    try:
        username = loginUserObj.idjinfo.djusername
        passwd = decodeStr(loginUserObj.idjinfo.djpasswd)
        print('*' * 88)
        print(username, passwd)
        run = Runner(username=username, password=passwd)
        userInfo = run.getCredItinfoToday()
        scores = run.getCredItinfo()
        print(scores)
        ret['scores'] = scores[1]
        ret['userinfo'] = userInfo
        ret['dailyInfo'] = dailyInfo
        ret['dailyDetail'] = dailyDetail

    except Exception as e:
        # 在这里return一个弹出页面提示没有党建云信息绑定用户
        print(e)

    return render(request, 'info.html', ret)


@csrf_exempt
def showDetail(request):
    loginUser = request.user.username

    ret = {
        'retmsg': '',
        'datas': None,
        'loginUser': loginUser,
        'sdatas': None,
    }
    try:
        loginUserObj = User.objects.get(username=loginUser)
    except Exception as e:
        loginUserObj = None
        print(e)

    if request.method == "GET":
        date = request.GET.get('date', None)
        # print(date)
        if date:
            detailObj = DailyDetail.objects.filter(create_day=date).filter(idjinfo=loginUserObj.idjinfo)
            ret['datas'] = detailObj
            ################################各项表格独立的########################################
            print('*8'*88)
            ret['thumbs'] = ThumbInfo.objects.filter(create_day=date).filter(idjinfo=loginUserObj.idjinfo)
            ret['studys'] = StudyInfo.objects.filter(create_day=date).filter(idjinfo=loginUserObj.idjinfo)
            ret['helps'] = HelpInfo.objects.filter(create_day=date).filter(idjinfo=loginUserObj.idjinfo)
            ret['views'] = ViewInfo.objects.filter(create_day=date).filter(idjinfo=loginUserObj.idjinfo)
            ret['exams'] = ExamInfo.objects.filter(create_day=date).filter(idjinfo=loginUserObj.idjinfo)
            print('*8'*88)
            # print(ret['sdatas'])


    return render(request, 'showDetail.html', ret)


@check_login
@csrf_exempt
def index(request):
    loginUser = request.user.username
    ret = {
        'loginUser': loginUser,
    }

    print(request.path)
    return render(request, 'index.html', ret)


######################################################################################################
# form表单
# 登录的django-from
class LogForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '用户名', 'required': 'required', }),
                               max_length=50, error_messages={'required': 'username不能为空', })
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '密 码', 'required': 'required', }),
        max_length=20, error_messages={'required': 'password不能为空', })
########################################################################################################
