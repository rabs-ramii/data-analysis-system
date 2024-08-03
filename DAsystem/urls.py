"""DAsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from DAsystem import views;

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homePage, name="homepage"),
    path('guest_user/', views.userhome, name="userhome"),
    path('guest_user/file/info/', views.fileinfo, name="fileinfo"),
    path('guest_user/file/desc/', views.filedesc, name="filedesc"),
    path('guest_user/first/5/row/', views.firstfive, name="firstfive"),
    path('guest_user/last/5/row/', views.lastfive, name="lastfive"),
    path('guest_user/isnull/', views.isnull, name="isnull"),
    path('guest_user/null/value/sum/', views.nullsum, name="nullsum"),
    path('guest_user/fill/all/null/', views.fillnull, name="fillnull"),
    path('guest_user/show/all/columns/', views.showcolumns, name="showcolumns"),
    path('guest_user/statistics/', views.statistic, name="statistic"),
    path('guest_user/scatterplot/', views.scatterplot, name="scatterplot"),
    path('guest_user/lineplot/', views.lineplot, name="lineplot"),
    path('guest_user/boxplot/', views.boxplot, name="boxplot"),
    path('guest_user/histogram/', views.histogram, name="histogram"),
    path('guest_user/logout/', views.logout, name="logout"),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
