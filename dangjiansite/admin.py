from django.contrib import admin

# Register your models here.
from dangjiansite.models import User, DjInfo, DailyResult, DailyDetail, ErrLog, ThumbLog, ExamDetail, ExamInfo, Qa

admin.site.register(User)
admin.site.register(DjInfo)
admin.site.register(DailyResult)
admin.site.register(DailyDetail)
admin.site.register(ErrLog)
admin.site.register(ThumbLog)
admin.site.register(ExamDetail)
admin.site.register(ExamInfo)
admin.site.register(Qa)
