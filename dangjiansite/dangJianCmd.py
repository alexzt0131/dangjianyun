import datetime
import os, django
import random
import re
import time

from dangjiansite.djfuncs import getAnswersFromFile
from dangjiansite.runner import Runner
from dangjiansite.views import getFormedDateStr, decodeStr, write2File

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dangjianyun.settings")
django.setup()
from dangjiansite import views
from dangjiansite.models import ThumbLog, User, DjInfo, DailyDetail, ExamInfo, Qa, ExamDetail, ErrLog, DailyResult, \
    StudyInfo, HelpInfo, ViewInfo, ThumbInfo
from dangjiansite.views import checkScore

# print(DjInfo.objects.get(djusername='024040').iuser)

#通过将user与djinfo互相外键 来重构系统  要在这里实现所有需要执行的方法。


# getDailyDetailObj 重写次函数 不要request参数实现

djusers = [i for i in DjInfo.objects.all()]
userobj = djusers[1].iuser
print(userobj)
run = Runner(username=userobj.idjinfo.djusername, password=decodeStr(userobj.idjinfo.djpasswd))

##################################settings##########################################
import logging

logging.basicConfig(level=logging.WARNING,
                    filename='./log/{}-log.txt'.format('dangJianCmd'),
                    filemode='a',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')



#######################################已完成的################################################
#已完成
def initQa():
    '''
    初始化一个题库
    :return:
    '''
    a = getAnswersFromFile()
    print(a)

    for i in a:
        Qa.objects.create(
            question=i[0],
            answer=i[1],
            answerText=i[2]
        ).save()
#已完成
def isFinish(userobj, run):
    '''
    检测传入用户是否完成了所有的程序
    :param userobj:
    :param run:
    :return:boolean
    '''
    scores = checkScore(run)
    for k, v in scores.items():
        # print(k, v)
        current = v.split('/')[0]
        total = v.split('/')[1]
        if current != total:
            return False
    return True

#已完成自循环 独立完成信息表
def exam(userobj, run):
    examTimes = run.getExcuteTimes()['exam']
    # current = checkScore(run)['exam'].split('/')[0]
    # total = checkScore(run)['exam'].split('/')[1]
    # print(current, total)
    # print(examTimes)
    # if current == total:
    #     print('无需做题操作')
    #     examTimes = 1  # <<<
    # for i in range(2):#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    while examTimes > 0:#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        run.doExam()  #
        #将结果写入数据库
        examDetail = run.examC19Info
        ExamDetail.objects.all().delete()
        ExamDetail.objects.create(
            idjinfo=userobj.idjinfo,
            subjectId=examDetail[0]['id'],
            title=examDetail[0]['title'],
            detail=examDetail[0]['detail'],

        )
        examInfo = run.qaList#qa = {'index': i['id'], 'answer': answer, 'answerText': answerText}
        for i in examInfo:
            question = Qa.objects.get(answerText=i['answerText']).question
            detail = '{} 问题： {}\n答案： {}-{}\n'.format(getFormedDateStr(), question, i['answerText'], i['answer'])
            dobj = getDailyDetailObj(userobj)
            try:
                dobj.examDetail += '{}<br/>'.format(detail)
            except Exception as e:
                dobj.examDetail = ''
                pass
            text = dobj.examDetail
            pat = r'<br/>'
            s = re.compile(pat).sub('', text)
            dobj.examDetail = s
            dobj.save()
            for i in examInfo:

                if len(ExamInfo.objects.filter(create_day=getFormedDateStr())) >= 20:
                    break
                else:
                    # print('*'*88)
                    # print(i['answerText'])
                    question = Qa.objects.get(answerText=i['answerText']).question
                    ExamInfo.objects.create(
                        idjinfo=userobj.idjinfo,
                        question=question,
                        answer=i['answer'],
                        answerText=i['answerText']).save()
            examTimes = run.getExcuteTimes()['exam']
            time.sleep(2)
    else:
        print('无需做题操作')

#已完成
def getDailyDetailObj(userobj):
    '''
    返回一个当日dailydetail对象，没有就创建一个返回
    :param userobj:
    :return:
    '''
    loginUser = userobj
    loginUserObj = None
    try:
        loginUserObj = User.objects.get(username=loginUser)
    except Exception as e:
        print(e)
    today = getFormedDateStr()
    dobj = DailyDetail.objects.filter(create_day=today).filter(idjinfo=loginUserObj.idjinfo)
    if not dobj:
        DailyDetail.objects.create(idjinfo=loginUserObj.idjinfo).save()
        return DailyDetail.objects.filter(create_day=today).filter(idjinfo=loginUserObj.idjinfo)[0]
    else:
        return dobj[0]

#已完成自循环独立完成信息表
def help(userobj, run):
    '''
    互助模块
    将结果写入文件
    :param run:
    :return:
    '''
    helpTimes = run.getExcuteTimes()['help']

    # current = checkScore(run)['help'].split('/')[0]
    # total = checkScore(run)['help'].split('/')[1]
    # if current == total:
    #     print('无需互助操作')
    #     helpTimes = 0
    # for i in range(2):
    while helpTimes > 0:
        print('还有{}个页面可选。'.format(len(run.helpPages)))
        print('debug out put.', run.helpPages)
        print('已经互助{}个'.format(len(run.helpedPages)))
        id = random.choice(run.helpPages)
        if id not in run.helpedPages:
            detail, log, helpInfo = run.doHelp(id=id)  # log暂时不知用不用

            ##############记录到单独表中###############

            HelpInfo.objects.create(
                idjinfo=userobj.idjinfo,
                title=helpInfo['title'],
                reply=helpInfo['reply'],
            ).save()
            ###############结果集合中##############

            dobj = getDailyDetailObj(userobj)
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
        helpTimes = run.getExcuteTimes()['help']
        time.sleep(2)
    else:
        print('无需互助操作')

#已完成自循环独立完成信息表
def viewPublic(userobj, run):
    '''
    发布党员视野
    :param run:
    :return:
    '''
    viewTimes = run.getExcuteTimes()['view']
    while viewTimes > 0:
    # for i in range(2):#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        print('已经发布{}个'.format(len(run.viewsResults)))
        detail, publicContent = run.doView()

        ##############记录到单独表中###############

        ViewInfo.objects.create(
            idjinfo=userobj.idjinfo,
            pub_content=publicContent,
        ).save()

        ##############记录到集体表中################


        dobj = getDailyDetailObj(userobj)
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
        viewTimes = run.getExcuteTimes()['view']
        time.sleep(2)
    else:
        print('无需党员视野发布操作')

#已完成自循环 独立完成信息表
#尝试不要循环时间，以后获取随机取学习主题(不循环不可行)
def study(userobj, run):
    '''
    判断执行次数操作，并将结果写入文件
    :param run:
    :return:
    '''
    studyTimes = run.getExcuteTimes()['study']
    while studyTimes > 0:
    # for i in range(1):#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
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
            result = "{} 学习主题: {}\n回复内容：\n{}\n".format(run.getCurrentTime(), run.studyRsults['title'], run.studyRsults['content'])
            # print(result)
            ##############记录到单独表中###############


            StudyInfo.objects.create(
                idjinfo=userobj.idjinfo,
                title=run.studyRsults['title'],
                reply=run.studyRsults['content'],
            ).save()




            ##############记录到集体表中################
            dobj = getDailyDetailObj(userobj)
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
        studyTimes = run.getExcuteTimes()['study']
    else:
        print('无需学习操作')

#已完成独立完成信息表
# 暂时可用，有待优化循环中的代码，再看看还有什么问题
def thumbTen(userobj, run):
    '''
    判断执行次数操作，并将结果写入文件
    :param run:
    :return:
    '''
    loginUser = userobj
    loginUserObj = None
    try:
        loginUserObj = User.objects.get(username=loginUser)
    except Exception as e:
        print(e)
        logging.exception("msg: {}.".format(str(e)))
    thumbTimes = run.getExcuteTimes()['thumb']


    # for i in range(10):#《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《
    while thumbTimes > 0:
        print('还有{}个页面可选。'.format(len(run.thumbPages)))
        print('debug out put.', run.thumbPages)
        print('已经点赞{}个'.format(len(run.thumbedPages) + 1))
        id = random.choice(run.thumbPages)
        thumbedSet = []
        thumbedSet.extend(run.thumbedPages)
        thumbedSet.extend(run.multiThumbed)
        thumbedSet.extend(run.thumbedFileList)
        thumbedId = [i.thumbId for i in ThumbLog.objects.filter(idjinfo=loginUserObj.idjinfo)]  # 数据多了会造成负担，需要想办法不要每次循环都这么做
        if id not in thumbedSet and id not in thumbedId:
            detail, thumbInfo = run.doThumb(id=id)
            ###############记录点过的###############
            ThumbLog.objects.create(
                idjinfo=loginUserObj.idjinfo,
                thumbId=id,
            ).save()

            ##############记录到单独表中###############

            ThumbInfo.objects.create(
                idjinfo=userobj.idjinfo,
                title=thumbInfo['title'],
                reply=thumbInfo['reply'],
            ).save()

            ##############记录到集体表中################



            dobj = getDailyDetailObj(userobj)
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
            thumbTimes = run.getExcuteTimes()['thumb']
            time.sleep(13)
        else:
            print('id {} 已经赞过。'.format(id))
    else:
        print('无需点赞操作')

#####################################################################################################
#从djinfo中便利出来的username
# for i in djusers:
#     print(i.iuser)








def main(userobj):


    # 初始化答案
    if len(Qa.objects.all()) == 0:
        initQa()

    run = Runner(username=userobj.idjinfo.djusername, password=decodeStr(userobj.idjinfo.djpasswd))

    try:
        thumbTen(userobj=userobj, run=run)
    except Exception as e:
        print(e)
        logging.exception("msg: {}.".format(str(e)))
        # ErrLog.objects.create(idjinfo=userobj.idjinfo, content=str(e))

    try:
        help(userobj=userobj, run=run)
    except Exception as e:
        print(e)
        logging.exception("msg: {}.".format(str(e)))
        # ErrLog.objects.create(idjinfo=userobj.idjinfo, content=str(e))

    try:
        viewPublic(userobj=userobj, run=run)
    except Exception as e:
        print(e)
        logging.exception("msg: {}.".format(str(e)))
        # ErrLog.objects.create(idjinfo=userobj.idjinfo, content=str(e))

    try:
        exam(userobj=userobj, run=run)
    except Exception as e:
        print(e)
        logging.exception("msg: {}.".format(str(e)))
        # ErrLog.objects.create(idjinfo=userobj.idjinfo, content=str(e))

    try:
        study(userobj=userobj, run=run)
    except Exception as e:
        print(e)
        logging.exception("msg: {}.".format(str(e)))
        # ErrLog.objects.create(idjinfo=userobj.idjinfo, content=str(e))


    try:
        if isFinish(userobj=userobj, run=run):
            print('in finish')

            flag = DailyResult.objects.filter(create_day=getFormedDateStr()).filter(idjinfo=userobj.idjinfo)

            if len(flag) == 0:#没有该用户当日的结果
                print('flag True')
                # 将结果写入当日的数据

                results = run.getCredItinfo()[1]
                print(results)
                DailyResult.objects.create(
                    idjinfo=userobj.idjinfo,
                    thumb=results['信息评论'],
                    view=results['党员视角发布'],
                    hlep=results['互助广场回答'],
                    exam=results['在线知识竞答'],
                    study1=results['在线阅读学习资料'],
                    study2=results['学习资料写体会'],
                    conLogin=results['连续登录'],
                    mobileLogin=results['手机端登录'],
                ).save()
                print('end..')
                pass
            else:
                print('{}当日详情已记录。'.format(userobj.idjinfo.djusername))

        else:
            print('*'*88)
            print('有未完成项目，重启main函数。')
            main(userobj)
    except Exception as e:
        print(e)
        logging.exception("msg: {}.".format(str(e)))















######################################backup#############################################################
#已完成
# def study(userobj, run):
#     '''
#     判断执行次数操作，并将结果写入文件
#     :param run:
#     :return:
#     '''
#     studyTimes = run.getExcuteTimes()['study']
#     current1 = checkScore(run)['study1'].split('/')[0]
#     total1 = checkScore(run)['study1'].split('/')[1]
#     current2 = checkScore(run)['study2'].split('/')[0]
#     total2 = checkScore(run)['study2'].split('/')[1]
#
#
#
#
#     # if current1 == total1 and current2 == total2:
#     if current1 == total1 and current2 == total2:
#         print('无需学习操作')
#         studyTimes = 0  # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#     for i in range(studyTimes):
#         print('还有{}个页面可选。'.format(len(run.studyPages)))
#         print('debug out put.', run.studyPages)
#         mid = random.choice(run.studyPages)
#         # 记录访问的标题与id
#         for i in run.studyPageList:
#             if mid == i[1]:
#                 run.studyRsults.update({'title': i[0]})
#         run.doStudy(mid=mid)
#     # 写入当日result文件
#     if run.studyRsults:
#         result = "{} 学习主题: {}\n回复内容：\n{}\n".format(run.getCurrentTime(), run.studyRsults['title'], run.studyRsults['content'])
#         print(result)
#         dobj = getDailyDetailObj(userobj)
#         try:
#             dobj.study1Detail += '{}<br/>'.format(result)
#         except Exception as e:
#             dobj.study1Detail = ''
#             pass
#         text = dobj.study1Detail
#         pat = r'<br/>'
#         s = re.compile(pat).sub('', text)
#         dobj.study1Detail = s
#         dobj.save()
#         write2File(run, './results/', 'result.txt', result)
#已完成自循环 独立表
# def exam(userobj, run):
#     examTimes = run.getExcuteTimes()['exam']
#     # current = checkScore(run)['exam'].split('/')[0]
#     # total = checkScore(run)['exam'].split('/')[1]
#     # print(current, total)
#     # print(examTimes)
#     # if current == total:
#     #     print('无需做题操作')
#     #     examTimes = 1  # <<<
#     for i in range(1):
#     # while examTimes > 0:
#         run.doExam()  #
#         #将结果写入数据库
#         examDetail = run.examC19Info
#         ExamDetail.objects.all().delete()
#         ExamDetail.objects.create(
#             idjinfo=userobj.idjinfo,
#             subjectId=examDetail[0]['id'],
#             title=examDetail[0]['title'],
#             detail=examDetail[0]['detail'],
#
#         )
#         examInfo = run.qaList
#         for i in examInfo:
#
#             if len(ExamInfo.objects.filter(create_day=getFormedDateStr())) >= 20:
#                 break
#             else:
#                 # print('*'*88)
#                 # print(i['answerText'])
#                 question = Qa.objects.get(answerText=i['answerText']).question
#                 ExamInfo.objects.create(
#                     idjinfo=userobj.idjinfo,
#                     question=question,
#                     answer=i['answer'],
#                     answerText=i['answerText']).save()
#         examTimes = run.getExcuteTimes()['exam']
#         time.sleep(2)
#     else:
#         print('无需做题操作')
##################################################################################################################




if __name__ == "__main__":
    date = getFormedDateStr()
    loginUserObj = userobj
    thumbs = ThumbInfo.objects.filter(create_day=date).filter(idjinfo=loginUserObj.idjinfo)
    studys = StudyInfo.objects.filter(create_day=date).filter(idjinfo=loginUserObj.idjinfo)
    helps = HelpInfo.objects.filter(create_day=date).filter(idjinfo=loginUserObj.idjinfo)
    views = ViewInfo.objects.filter(create_day=date).filter(idjinfo=loginUserObj.idjinfo)
    exams = ExamInfo.objects.filter(create_day=date).filter(idjinfo=loginUserObj.idjinfo)

    for i in a:
        print(i)
    print("*"*88)
    for i in b:
        print(i)
    print("*"*88)
    for i in c:
        print(i)
    print("*"*88)
    for i in d:
        print(i)
    print("*"*88)
    for i in e:
        print(i)
    print("*"*88)
    # main(userobj)
    # print(datetime.datetime.now().strftime("%H:%M:%S"))
    pass



