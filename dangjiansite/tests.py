import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dangjianyun.settings")
django.setup()
from dangjiansite.models import Qa, ThumbLog, User

# correctAnswer = Qa.objects.filter(question__contains='推进_____，建设覆盖纪检监察系统的检举举报平台。强化不敢腐的震慑，扎牢不能腐的笼子，增强不想腐的自觉，通过不懈努力换来海晏河清、朗朗乾坤。')[0]
# answerText = correctAnswer.answerText
# answer = correctAnswer.answer
#
# print(answerText, answer)
#
loginUserObj = User.objects.get(username='4040')
thumbedId = [i.thumbId for i in ThumbLog.objects.filter(idjinfo=loginUserObj.idjinfo)]
# Qa.objects.all().delete()
id = '473268'
if not ThumbLog.objects.filter(thumbId=id):
    print('not exists')
else:
    print('exists')