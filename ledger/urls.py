from django.conf.urls import url

from . import views

app_name = 'ledger'
urlpatterns = [
    # ex: /ledger/
    url(r'^$', views.index, name='index'),
    # ex: /ledger/bob/
    url(r'^(?P<friend_id>[a-z]+)/$', views.friend, name='friend'),
]
