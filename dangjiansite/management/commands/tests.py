import os, django

from dangjiansite.djfuncs import getAnswersFromFile
from dangjiansite.runner import Runner

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dangjianyun.settings")
django.setup()
from dangjiansite.models import Qa

# correctAnswer = Qa.objects.filter(question__contains='推进_____，建设覆盖纪检监察系统的检举举报平台。强化不敢腐的震慑，扎牢不能腐的笼子，增强不想腐的自觉，通过不懈努力换来海晏河清、朗朗乾坤。')[0]
# answerText = correctAnswer.answerText
# answer = correctAnswer.answer
#
# print(answerText, answer)
#

run = Runner(username='024549', password='Aa1234')
viewTimes = run.getExcuteTimes()

print(viewTimes)