from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /ledger/
    url(r'^$', views.index, name='index'),
    # ex: /ledger/bob/
    url(r'^(?P<friend_id>[a-z]+)/$', views.friend, name='friend'),
]
