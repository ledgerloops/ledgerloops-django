from django.conf.urls import url

from . import views

app_name = 'ledger'
urlpatterns = [
    # ex: /ledger/
    url(r'^$', views.friend_list, name='index'),
    # ex: /ledger/1/
    url(r'^(?P<pk>[0-9]+)/$', views.entry_list, name='friend'),
    # ex: /ledger/1/add
    url(r'^(?P<pk>[0-9]+)/add$', views.add, name='add'),
]
