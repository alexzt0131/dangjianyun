import json
import os, django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dangjianyun.settings")# project_name 项目名称
django.setup()
from dangjiansite.djfuncs import *
import os
import datetime
import requests
import time
import urllib3
import base64
import csv
import random
from bs4 import BeautifulSoup
from dangjiansite.models import *










class Runner():

    # def __init__(self, appid='TJZHDJ01', username='024549', password='Aa1234'):
    def __init__(self, appid='TJZHDJ01', username='', password=''):
        urllib3.disable_warnings()#屏蔽ssl告警
        self.currentTime = datetime.datetime.now().strftime("%H:%M:%S")
        self.username = username
        self.password = password
        self.thumbedFilePath = './lib/'.format(username)
        self.logFilePath = './log/'.format(username)
        self.errFilePath = './err/'.format(username)
        # self.thumbedFileList = self.getThumbFromFile()
        self.thumbedFileList = []
        self.debug = True
        self.session = requests.session()
        self.appid = appid#应该是本设备安装app的id 等换个设备试一下就知道了
        self.headers ={
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; HUAWEI MLA-AL10 Build/HUAWEIMLA-AL10)',
            'header_version': '80',
            'system': 'android',
            'Connection': 'Keep-Alive',
            'Host': 'mapi.dangjianwang.com',
        }
        self.token = self.getToken()
        time.sleep(0.1)
        self.thumbPageList = self.getPages(urls=[
            'https://mapi.dangjianwang.com/v3_1/Learn/List',
            'https://mapi.dangjianwang.com/v3_1/Activities/List',
            'https://mapi.dangjianwang.com/v3_1/Hotspots/Hotlist'
        ])
        self.thumbPages = [i[1] for i in self.thumbPageList]
        time.sleep(0.1)
        self.helpPageList = self.getPages(urls=['https://mapi.dangjianwang.com/v3_1/Help/List', ])
        self.helpPages = [i[1] for i in self.helpPageList]
        self.helpResults = {}
        time.sleep(0.1)
        self.studyPageList = self.getPagesII(urls=['https://mapi.dangjianwang.com/v3_1/Study/MaterialCollList'])
        self.studyPages = [i[1] for i in self.studyPageList]
        time.sleep(0.1)
        self.studyRsults = {}
        self.thumbedPages = []
        self.thumbResults = {}
        self.helpedPages = []
        self.multiThumbed = []#考虑最后要写入文件之中
        self.viewsResults = []
        self.examC19Info = []
        self.examlist = []
        self.qaList = []

    def getCurrentTime(self):
        return datetime.datetime.now().strftime("%H:%M:%S")


    def writeErr2File(self, err):
        path = self.logFilePath
        fullPath = '{}{}err.txt'.format(path, self.username)
        if not os.path.exists(path):
            os.mkdir(path)
        with open(fullPath, 'a') as f:
            f.write('{}:{}\n'.format(self.currentTime, err))
        print('err已经写入{}'.format(fullPath))

    def writeLog2File(self, log):
        path = self.logFilePath
        fullPath = '{}{}logs.txt'.format(path, self.username)
        if not os.path.exists(path):
            os.mkdir(path)
        with open(fullPath, 'a') as f:
            f.write('{}:{}\n'.format(self.currentTime, log))
        print('log已经写入{}'.format(fullPath))

    def writeThumb2File(self, id):
        path = self.thumbedFilePath
        fullPath = '{}{}thumbs.txt'.format(path, self.username)
        if not os.path.exists(path):
            os.mkdir(path)
        with open(fullPath, 'a') as f:
            f.write(',{}'.format(id))
        print('点赞记录已经写入{}'.format(fullPath))

    def getThumbFromFile(self):
        '''

        :return: 文件中id组成的列表
        '''
        path = self.thumbedFilePath
        inFileList = []
        fullPath = '{}{}thumbs.txt'.format(path, self.username)
        if not os.path.exists(fullPath):
            return fullPath
        with open(fullPath, 'r') as f:
            inFileList.extend(list(set(f.readlines()[0].split(','))))
        #     print('getThumbFormFile', inFileList)
        with open(fullPath, 'w') as f1:
            f1.write(','.join(sorted(inFileList)))
        return inFileList

    def getExcuteTimes(self):
        '''
        返回点赞等自动执行的次数的字典
        :return:
        '''
        excuteTimes = {}

        credInfo = self.getCredItinfo()
        print(credInfo)
        currentScore = credInfo[0]

        # 点赞次数
        thumbScore = credInfo[1]['信息评论'].split('/')[0]
        thumbExcuteTimes = 10 - int(thumbScore)
        excuteTimes.update({'thumb': thumbExcuteTimes})
        # 帮助次数
        helpScore = credInfo[1]['互助广场回答'].split('/')[0]
        helpExctuteTimes = 2 - int(helpScore)
        excuteTimes.update({'help': helpExctuteTimes})
        # 党员视角发布次数
        viewScore = credInfo[1]['党员视角发布'].split('/')[0]
        viewExcuteTimes = int((4 - int(viewScore)) / 2)
        excuteTimes.update({'view': viewExcuteTimes})
        # 在线知识竞答次数
        examScore = credInfo[1]['在线知识竞答'].split('/')[0]
        examExcuteTimes = int((4 - int(examScore)) / 2)
        excuteTimes.update({'exam': examExcuteTimes})
        # 学习次数
        flag = int(credInfo[1]['在线阅读学习资料'].split('/')[1]) - int(credInfo[1]['在线阅读学习资料'].split('/')[0])
        flag1 = int(credInfo[1]['学习资料写体会'].split('/')[1]) - int(credInfo[1]['学习资料写体会'].split('/')[0])
        examExcuteTimes = 1 if flag != 0 or flag1 != 0 else 0
        excuteTimes.update({'study': examExcuteTimes})

        return excuteTimes

    def getToken(self):
        '''
        获得一个连接的token
        每个连接都需要使用到
        :return:
        '''
        data = {
            'appid': self.appid,
            'username': self.username,
            'password': self.password,
        }
        longinurl = 'https://mapi.dangjianwang.com/v3_1/login'

        r = self.session.post(url=longinurl, data=data, verify=False)
        rjson = r.json()
        # print(type(rjson))
        # print(rjson)

        if rjson['code'] == '200':
            return rjson['token']
        else:
            print('token 获得失败')
            return None

    def getRJson(self, url):
        data={
            'token': self.token,
            'appid': self.appid
        }

        return self.session.post(url=url, data=data, verify=False).json()

    def getUserInfo(self):
        '''
        获得一大串用户的信息，暂时没用
        :return:
        '''
        infoUrl = 'https://mapi.dangjianwang.com/v3_1/User/UserInfo'
        return self.getRJson(url=infoUrl)

    def getCredItinfoToday(self):
        '''
        获得人员当前的得分等级参数
        :return:
        '''
        creditInfourl = 'https://mapi.dangjianwang.com/v3_1/User/CreditInfo'
        info = self.getRJson(url=creditInfourl)
        fullScore = info['data']['full']
        gainScore = info['data']['gain']
        currentLevel = info['data']['level']
        username = info['data']['name']
        ret = {
            'fullScore': fullScore,
            'gainScore': gainScore,
            'currentLevel': currentLevel,
            'username': username,
        }
        return ret


    def getCredItinfo(self):
        '''
        获得用户的今日积分状态
        可用来判断是否需要再继续流程
        数据如下
        ('35', [('连续登录', '3/3'), ('手机端登录', '2/2'), ('信息评论', '10/10'), ('党员视角发布', '4/4'), ('互助广场回答', '2/2'), ('学习资料写体会', '5/5'), ('在线阅读学习资料', '5/5'), ('在线知识竞答', '4/4')])
        :return:(haved_credit, credit_detail)
        '''
        creditInfourl = 'https://mapi.dangjianwang.com/v3_1/User/CreditInfo'
        haved_credit = 0
        credit_detail = {}

        info = self.getRJson(url=creditInfourl)
        for k, v in info.items():
            if k == 'data':
                for k2, v2 in v.items():
                    if k2 == 'haved_credit':
                        haved_credit = v2
                    if k2 == 'credit_detail':
                        for i in v2:
                            credit_detail.update({i['title']: i['score']})

        return (haved_credit, credit_detail)

    def getPages(self, urls):
        pages = []
        for url in urls:
            data = self.getRJson(url=url)
            for k, v in data.items():
                if k == 'data':
                    for i in v:
                        # pages.append({'pageId': i['id'], 'pageTitle': i['title']})
                        # pages.append(i['id'])
                        pages.append((i['title'], i['id']))

        return pages

    def getPagesII(self, urls):
        def getRJson(url):
            data = {
                'token': self.token,
                'appid': self.appid,
                'type_id': '791',
                'page_index': '1',
            }

            return self.session.post(url=url, data=data, verify=False).json()
        pages = []
        for url in urls:
            data = getRJson(url=url)
            for k, v in data.items():
                # print(k, v)
                if k == 'data':
                    for i in v:
                        # pages.append({'pageId': i['id'], 'pageTitle': i['title']})
                        # pages.append(i['id'])
                        pages.append((i['name'], i['id']))

        return pages

    def doThumb(self, id):
        '''
        点赞函数，操作与id对应的页面
        每次记录对应的信息到文件
        :return:
        '''
        contents = [
            '关注',
            '关注！',
            '关注！！']
        data = {
            'id': id,
            'comment': random.choice(contents),
            'token': self.token,
            'appid': self.appid,
        }
        commitUrl = 'https://mapi.dangjianwang.com/v3_1/Activities/CommentAct'
        rjson = self.session.post(url=commitUrl,
                                 data=data,
                                 verify=False).json()
        print(rjson)
        if rjson['code'] == '1003':
            self.token = self.getToken()
        elif rjson['code'] == '200':
            result = rjson['msg']
            if result == '操作成功':
                self.thumbedPages.append(id)
                # print(self.thumbPageList)
                # print(len(self.thumbPageList), len(list(set(self.thumbPageList))))

                for i in list(set(self.thumbPageList)):
                    if id == i[1]:
                        temp = {'title': i[0]}
                        self.thumbResults.update(temp)
                        log = '信息点赞：\n主题: {}\n提交：{}'.format(i[0], data['comment'])
                        detail = '{} 主题:{}\n回复:{}\n'.format(self.getCurrentTime(), i[0], data['comment'])
                        write2File(self, './results/', 'result.txt', log)
                        thumbInfo = {'title': i[0], 'reply': data['comment']}

                self.thumbPages.remove(id)
                self.writeThumb2File(id=id)

                return (detail, thumbInfo)
        elif rjson['code'] == '500' and rjson['msg'] == '评论过快，请求休息一会':
            print('因评论过快，等待一段时间')
            time.sleep(20)
        else:
            print('rjson', rjson)
            # self.multiThumbed.append(id)
            self.thumbedPages.remove(id)#不成功的时候也要去掉不然总会选到
            self.writeThumb2File(id=id)
        log = '点赞：{}'.format(rjson)
        self.writeLog2File(log)
        print(log)
        time.sleep(10)


    def doHelp(self, id, callback=None):
        '''
        互助功能
        :param id:
        :return:
        '''
        detail = ''
        helpInfo = None
        log = ''
        content = [
            '把党的政治建设摆在首位!',
            '不忘初心，牢记使命！',
            '发展史第一要务，人才是第一资源，创新是第一动力。',
            '要把党的领导贯彻到依法治国全过程和各方面',
            '毫不动摇坚持中国共产党领导',]
        data = {
            'id': id,
            'content': random.choice(content),
            'token': self.token,
            'appid': self.appid,
        }
        print(data)
        commitUrl = 'https://mapi.dangjianwang.com/v3_1/Help/PostComment'
        rjson = self.session.post(url=commitUrl,
                                  data=data,
                                  verify=False).json()



        if rjson['code'] == '200':
            result = rjson['msg']
            if result == '操作成功':
                self.helpedPages.append(id)
                self.helpPages.remove(id)
                #记录成功的到result
                for i in self.helpPageList:
                    if id == i[1]:
                        curTime = self.getCurrentTime()
                        # print('('*88)
                        # print(curTime)
                        self.helpResults.update({'title': id[0]})
                        log = '互助:\n主题： {}\n提交内容： {}'.format(i[0], rjson['comment'])
                        write2File(self, './results/', 'result.txt', log)
                        # #写入数据库
                        detail = '{} 主题： {}\n提交内容： {}\n'.format(curTime, i[0], rjson['comment'].strip())
                        helpInfo = {'title': i[0], 'reply': rjson['comment']}
            else:
                pass
        else:
            pass

        log = '帮助：{}'.format(rjson)
        self.writeLog2File(log)
        print(log)
        return (detail, log, helpInfo)

    def doView(self):
        '''
        党员视角发布功能

        :return:
        '''

        content = [
            '全面的小康，覆盖的人口要全面，是惠及全体人民的小康。',
            '不忘初心，牢记使命，坚持终身学习！']
        data = {
            'content': random.choice(content),
            'token': self.token,
            'appid': self.appid,
        }
        commitUrl = 'https://mapi.dangjianwang.com/v3_1/Viewpoint/Create'
        rjson = self.session.post(url=commitUrl,
                                  data=data,
                                  verify=False).json()
        if rjson['code'] == '200':
            result = rjson['msg']
            if result == '操作成功':
                self.viewsResults.append(1)
                # self.viewsResults.append(id)
        else:
            pass

        log = '党员视角：{}'.format(rjson)
        detail = '{} 党员视角:\n发布内容:{}\n'.format(self.getCurrentTime(), rjson['data']['content'])
        publicContent = rjson['data']['content']
        # print(detail)
        # self.writeLog2File(log)
        # print('党员视角'*12)
        # print(id)
        # print(log)
        # print('党员视角' * 12)
        return (detail, publicContent)

    def doStudy(self, mid):
        '''
        前三个post函数的响应的三个请求
        get用来获得填写的内容
        最后一个post是学习完离开并检测时间的函数如果成功说明该次学习成功。
        :param mid:
        :return:
        '''
        interval = 60 * 5 + 5
        def post1():
            data = {
                'mid': mid,
                'token': self.token,
                'appid': self.appid,
            }
            commitUrl = 'https://mapi.dangjianwang.com/v3_1//Study/CheckCollStatus'
            rjson = self.session.post(url=commitUrl,
                                      data=data,
                                      verify=False).json()
            # print(rjson)
            log = '学习post1：{}'.format(rjson)
            self.writeLog2File(log)
            print(log)
        def post2():
            data = {
                'token': self.token,
                'appid': self.appid,
            }
            commitUrl = 'https://mapi.dangjianwang.com/v3_1/Login/CheckToken'
            rjson = self.session.post(url=commitUrl,
                                      data=data,
                                      verify=False).json()
            # print(rjson)
            log = '学习post2：{}'.format(rjson)
            self.writeLog2File(log)
            print(log)
        def post3():
            data = {
                'mid': mid,
                'token': self.token,
                'appid': self.appid,
            }
            commitUrl = 'https://mapi.dangjianwang.com/v3_1/Study/GetFeelingsNum'
            rjson = self.session.post(url=commitUrl,
                                      data=data,
                                      verify=False).json()
            # print(rjson)
            log = '学习post3：{}'.format(rjson)
            self.writeLog2File(log)
            print(log)

        def get1():
            url = 'https://mapi.dangjianwang.com/v3_1/Study/MaterialDetail?token={}&mid={}'.format(self.token, mid)
            rjson = self.session.get(url=url)
            text = rjson.content
            soup = BeautifulSoup(text, 'html.parser')
            retContents = []
            for div in soup.find_all('p'):
                p = div.text.strip()
                retContents.append(p if 100 > len(p) < 200 else p[0:200])
            return random.choice(retContents)

        def recordFeeling(content=None):
            if not content:
                content = '伟大的时代造就伟大的人物。邓小平同志就是从中国人民和中华民族近代以来伟大斗争中产生的伟人，' \
                          '是我们大家衷心热爱的伟人。我们很多同志都曾经在他的领导和指导下工作过，他的崇高风范对我们来说是那样熟悉、那样亲切。' \
                          '邓小平同志崇高鲜明又独具魅力的革命风范，将激励我们在实现“两个一百年”奋斗目标、实现中华民族伟大复兴中国梦的征程上奋勇前进。'
            data = {
                'mid': mid,
                'token': self.token,
                'appid': self.appid,
                'content': content
            }

            commitUrl = 'https://mapi.dangjianwang.com/v3_1/Study/RecordFeeling'
            rjson = self.session.post(url=commitUrl,
                                      data=data,
                                      verify=False).json()
            # print(rjson)
            log = '学习recordFeeling：{}'.format(rjson)
            self.writeLog2File(log)
            print('in recordFeeling')
            print(log)

            if rjson['code'] == '200':
                return {'content': content}
            elif rjson['code'] == '1120':
                addtion = [
                    '我们必须坚定不移，任何时候任何情况下都不能动摇',
                    '人民有信心，国家才有未来，国家才有力量。',
                    '新时代，属于自强不息、勇于创造的奋斗者。',
                    '民主政治建设有序推进，依法治市迈出新步伐。',
                    '一切公职人员，都必须牢记始终为人民利益和幸福而努力工作。',

                ]
                return recordFeeling(content= '{}\n{}'.format(content, random.choice(addtion)))
            else:
                return None
            #记录回复的心得


        def readTime():
            data = {
                'mid': mid,
                'token': self.token,
                'appid': self.appid,
                'time': interval,
            }
            commitUrl = 'https://mapi.dangjianwang.com/v3_1/Study/ReadTime'
            rjson = self.session.post(url=commitUrl,
                                      data=data,
                                      verify=False).json()
            # print(rjson)
            log = '学习readTime：{}'.format(rjson)
            # self.studyRsults.update({'学习readTime', rjson})
            self.writeLog2File(log)
            print(log)



        post1()
        time.sleep(1)
        post2()
        time.sleep(1)
        post3()
        time.sleep(1)
        content = get1()
        time.sleep(1)
        # time.sleep(interval)
        count = 0
        print('开始学习请稍后')
        for i in range(interval):
            count += 1
            # print(i + 1)
            if count % 30 == 0:
                print('已用时{}秒'.format(count))
            time.sleep(1)
        # time.sleep(5)
        print('填写的学习体会', content)
        self.studyRsults.update(recordFeeling(content=content))
        time.sleep(1)
        readTime()
        time.sleep(1)
        pass

    def doExam(self):
        '''

        :param self:
        :return:
        '''
        ids = []
        data = {
            'page': '1',
            'page_size': '20',
            'token': self.token,
            'appid': self.appid,
        }
        examlistUrl = 'https://mapi.dangjianwang.com/v3_1/quora/examlist'
        rjson = self.session.post(url=examlistUrl,
                                  data=data,
                                  verify=False).json()
        # print(rjson)
        # for i in rjson['data']:
        #     print(i)
        time.sleep(0.3)
        #########################################################
        print('*' * 99)
        data = {
            'page': '1',
            'page_size': '20',
            'token': self.token,
            'appid': self.appid,
        }
        banklistUrl = 'https://mapi.dangjianwang.com/v3_1/exam/banklist'
        rjson = self.session.post(url=banklistUrl,
                                  data=data,
                                  verify=False).json()
        # print(rjson)
        for i in rjson['data']:
            tem = (i['bank_name'], i['id'])
            self.examlist.append(tem)
            if i['bank_name'] == '十九大报告100题（单选）':
            # if i['bank_num'] == '65':
                temp = {
                    'title': i['bank_name'],
                    'detail': i['detail'],
                    'id': i['id'],
                }
                self.examC19Info.append(temp)
        # print(self.examC19Info)
        # print(self.examlist)
        time.sleep(0.3)
        #########################################################
        print('*' * 99)
        data = {
            'bank': '6',
            'token': self.token,
            'appid': self.appid,
        }
        commitUrl = 'https://mapi.dangjianwang.com/v3_1/exam/randexam'
        rjson = self.session.post(url=commitUrl,
                                  data=data,
                                  verify=False).json()
        # print(rjson)
        aa = rjson['data']
        paper = aa['id']
        for i in aa['questions']:
            temp = {'id': i['id'], 'content': i['content']}
            ids.append(temp)

        #########################################################
        print('*' * 99)
        time.sleep(0.5)
        # 以下答题交卷

        answers = []
        # 先得到答案


        for i in ids:
            # 丛书据库获得答案
            correctAnswer = Qa.objects.filter(question__contains=i['content'])[0]
            answerText = correctAnswer.answerText
            answer = correctAnswer.answer
            #从文键获得答案
            # answerText = getAnswer(i['content'])[2]
            # answer = getAnswer(i['content'])[1]
            temp = {'index': i['id'], 'answer': answer}
            qa = {'index': i['id'], 'answer': answer, 'answerText': answerText}
            self.qaList.append(qa)
            print(qa, i['content'])
            answers.append(temp)
            time.sleep(1)
        hdata = {
            'token': self.token,
            'appid': self.appid,
            'paper': paper,
            'answers': json.dumps(answers),
            # 'answers': [{'answer': 'A', 'index': '639'}, {'answer': 'A', 'index': '639'}],
        }
        # print('hdata:', hdata)
        commitUrl = 'https://mapi.dangjianwang.com/v3_1/exam/handpaper'
        rjson = self.session.post(url=commitUrl,
                                  data=hdata,
                                  verify=False).json()
        print(rjson)
        print(self.examlist)
        print(self.examC19Info)
        print(self.qaList)








    def getAnswerInfo(self):
        '''
        获得答题的结果与正确率
        :return:
        '''
        data = {
            'token': self.token,
            'appid': self.appid,
            'page_size': '20',
            'page_index': 'page_index',
        }
        commitUrl = 'https://mapi.dangjianwang.com/v3_1/exam/randexam'
        rjson = self.session.post(url=commitUrl,
                                  data=data,
                                  verify=False).json()
        print(rjson)


'''

https://mapi.dangjianwang.com/v3_1/exam/randexam  答题地址 主id是交卷的paper 这里要获取到questions里的id 等于回答问题中的index 
appid	TJZHDJ01
bank	6
token	5jTY47PbPZ0KdUprwmfJVfH4cX23tyDcV25XrEYkWVvElH3YjJpIb1JCDwq_

https://mapi.dangjianwang.com/v3_1/exam/handpaper  交卷的连接
appid	TJZHDJ01
answers	[{"index":"635","answer":"D"},{"index":"640","answer":"C"},{"index":"641","answer":"B"},{"index":"665","answer":"B"},{"index":"670","answer":"B"},{"index":"673","answer":"B"},{"index":"677","answer":"C"},{"index":"682","answer":"B"},{"index":"684","answer":"C"},{"index":"690","answer":"A"}]
token	5jTY47PbPZ0KdUprwmfJVfH4cX23tyDcV25XrEYkWVvElH3YjJpIb1JCDwq_
paper	4565894

https://mapi.dangjianwang.com/v3_1/exam/banklist 获得答题情况的连接

appid	TJZHDJ01
page_size	20
token	5jTY47PbPZxXeRxlkzScAPWidyvssy3TBD5Y9UYiCQnMmCfa2pRNb1JCDwq_
page_index	1




--------------------------------------------------
https://mapi.dangjianwang.com/v3_1/Study/MaterialCollList 学习的id列表
appid	TJZHDJ01
page_size	20
type_id	791
token	5jTY47PbPZJbeh9ixjfOUvaoI3604SrSAz5Zokt3DAmfz3qIis4Yb1JCDwq_
page_index	1

下面是针对791id列表中的访问地址
https://mapi.dangjianwang.com/v3_1//Study/CheckCollStatus

post1：
appid	TJZHDJ01
mid	9729
token	5jTY47PbPZoOKEUwlDCaAKWqICGwt3_OVzlVpk5yW1bMyS_M3J5Db1JCDwq_
post2：

https://mapi.dangjianwang.com/v3_1/Login/CheckToken
appid	TJZHDJ01
token	5jTY47PbPZoOKEUwlDCaAKWqICGwt3_OVzlVpk5yW1bMyS_M3J5Db1JCDwq_

post3：
https://mapi.dangjianwang.com/v3_1/Study/GetFeelingsNum
appid	TJZHDJ01
mid	9729
token	5jTY47PbPZoOKEUwlDCaAKWqICGwt3_OVzlVpk5yW1bMyS_M3J5Db1JCDwq_

get1 https://mapi.dangjianwang.com/v3_1/Study/MaterialDetail?token={}&mid={} 获得页面



post 发表体会
https://mapi.dangjianwang.com/v3_1/Study/RecordFeeling
appid	TJZHDJ01
content	 伟大的时代造就伟大的人物。邓小平同志就是从中国人民和中华民族近代以来伟大斗争中产生的伟人，是我们大家衷心热爱的伟人。我们很多同志都曾经在他的领导和指导下工作过，他的崇高风范对我们来说是那样熟悉、那样亲切。邓小平同志崇高鲜明又独具魅力的革命风范，将激励我们在实现“两个一百年”奋斗目标、实现中华民族伟大复兴中国梦的征程上奋勇前进。
mid	9729
token	5jTY47PbPckOdUlllmfOCaCvcy7ls3rSVmxRoE0gDg3EmyrYi5Ucb1JCDwq_

post 结束学习 
https://mapi.dangjianwang.com/v3_1/Study/ReadTime
appid	TJZHDJ01
time	362
mid	9729
token	5jTY47PbPckOdUlllmfOCaCvcy7ls3rSVmxRoE0gDg3EmyrYi5Ucb1JCDwq_


---------------------------------------

https://mapi.dangjianwang.com/v3_1/Help/List 这里获得帮助id
https://mapi.dangjianwang.com/v3_1/Help/PostComment 提交评论的地址


appid	TJZHDJ01
content	不忘初心，牢记使命!
id	55984
token	5jTY47PbPcpZe0s1xDLKAqKoIimx6SnSVjcApB92DF3Nmy/djZ1Nb1JCDwq_

把党的政治建设摆在首位！
不忘初心，牢记使命！

-------------------------------

发布的内容
https://mapi.dangjianwang.com/v3_1/Viewpoint/Create

appid	TJZHDJ01
content	不忘初心牢记使命
token	5jTY47PbPZ9deR5rkTXIB/b/fymw5HvbAj9R900gDArNnXqE1s9Kb1JCDwq_


不忘初心，牢记使命，坚持终身学习！
全面的小康，覆盖的人口要全面，是惠及全体人民的小康。

-----------------------------
点赞错误
{'msg': '重复评论过多，请您修改后重新提交。', 'code': '500'}
'''