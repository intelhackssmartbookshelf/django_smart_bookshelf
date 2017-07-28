"""django_smart_bookshelf URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from bookshelf.views import api_saveSelf, api_saveToken, api_sendMsg, api_saveTotalLength, BooksViewSet, api_getBookshelf
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'books', BooksViewSet, base_name='Booklist')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/shelf/', include(router.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^', include(router.urls)),
    url(r'^location/', api_saveSelf),
    url(r'^fcmtoken/', api_saveToken),
    url(r'^send_msg/', api_sendMsg),
    url(r'^set_totallen/', api_saveTotalLength),
    url(r'^bookshelf/', api_getBookshelf),
]
