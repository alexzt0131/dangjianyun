'''
需要requests、bs4
获得用户信息积分总数与等级
https://mapi.dangjianwang.com/v3_1/User/GetUserCredit HTTP/1.1
appid	TJZHDJ01
token	4DTb4LHEJc0NdURhxDedU6WsIivgtC_OUD4EoUcnXAnPnibYi5pXc01fEhQ=
'''
import base64
import csv
import datetime
import random

import os
import re




def viewPublic(run):
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
        run.doView()

def help(run):
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
            run.doHelp(id=id)

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

def thumbTen(run):
    '''
    判断执行次数操作，并将结果写入文件
    :param run:
    :return:
    '''
    thumbTimes = run.getExcuteTimes()['thumb']
    current = checkScore(run)['thumb'].split('/')[0]
    total = checkScore(run)['thumb'].split('/')[1]
    # print(current, total)
    # if thumbTimes == 0:
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
        if id not in thumbedSet:
            detail = run.doThumb(id=id)
        else:
            print('id {} 已经赞过。'.format(id))

def study(run):
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
        studyTimes = 0
    for i in range(studyTimes):
        print('还有{}个页面可选。'.format(len(run.studyPages)))
        print('debug out put.', run.studyPages)
        mid = random.choice(run.studyPages)
        #记录访问的标题与id
        for i in run.studyPageList:
            if mid == i[1]:
                run.studyRsults.update({'title': i[0]})
        run.doStudy(mid=mid)
    #写入当日result文件
    if run.studyRsults:
        result = "学习：{}".format(run.studyRsults)
        write2File(run, './results/', 'result.txt', result)

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
    filePath = './answers/new19.csv'#生产环境中要改为绝对路径
    if not os.path.exists(filePath):
        filePath = '/root/www/dangjianyun/dangjiansite/answers/new19.csv'

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

def exam(run):
    examTimes = run.getExcuteTimes()['exam']
    current = checkScore(run)['exam'].split('/')[0]
    total = checkScore(run)['exam'].split('/')[1]
    print(current, total)
    print(examTimes)
    if current == total:
        print('无需做题操作')
    # for i in range(examTimes):
    run.doExam()#次函数有问题500 失败

def encodeStr(str):
    return base64.b64encode(bytes(str, encoding='utf8'))
def decodeStr(bytes):
    return base64.b64decode(bytes).decode('utf8')

def getFormedDateStr():
    return datetime.datetime.now().strftime("%Y-%m-%d")


if __name__ == "__main__":
    # run = Runner()
    # a = run.getCredItinfoToday()
    # print(a)
    # run = Runner()

    pass
