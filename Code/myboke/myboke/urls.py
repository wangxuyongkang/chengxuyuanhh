"""myboke URL Configuration

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
from bokeapp import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/(?P<version>[v1|v2]+)/register/$',views.RegisterView.as_view({'post':'create'})),
    url(r'api/(?P<version>[v1|v2]+)/login/$',views.LoginView.as_view()),
    url(r'api/(?P<version>[v1|v2]+)/category/',views.CategaryView.as_view({'get':'list'})),
    url(r'api/(?P<version>[v1|v2]+)/list/(?P<pk>\d+)/$',views.BokelistView.as_view({'get':'list'}),name='list'),
    url(r'api/(?P<version>[v1|v2]+)/listall/$',views.BokelistallView.as_view({'get':'list'}),name='listall'),
    url(r'api/(?P<version>[v1|v2]+)/detail/(?P<pk>\d+)/',views.BokedetailView.as_view({'get':'list'}),name='detail'),
    url(r'api/(?P<version>[v1|v2]+)/comments/$',views.CommentsView.as_view({'post':'create'})),
    url(r'api/(?P<version>[v1|v2]+)/commentlist/(?P<pk>\d+)/$',views.CommentlistsView.as_view({'get':'list'})),
]
