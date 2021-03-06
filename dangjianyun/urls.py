"""dangjianyun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static


from dangjiansite.views import adduser, do_login, info, index, config, functions, do_logout, showDetail
from dangjianyun import settings 
urlpatterns = [
    url(r'^search/', admin.site.urls),
    url(r'^login/$', do_login),
    url(r'^index/$', index),
    url(r'^config/$', config),
    url(r'^functions/', functions),
    url(r'^logout/$', do_logout),
    url(r'^info/$', info),
    url(r'^showDetail/', showDetail),
    # url(r'^adduser/', adduser),
    # url(r'^$', do_login),
]
from django.conf import settings 
# if settings.DEBUG is False:
#     urlpatterns += patterns('',
#         url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT,
#         }),
#     )
if settings.DEBUG:    
    urlpatterns += patterns('',
 url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
 {'document_root': os.path.join(settings.SITE_ROOT,'media')},name="media"),
    )
