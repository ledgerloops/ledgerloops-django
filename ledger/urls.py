from django.conf.urls import url

from . import views

app_name = 'ledger'
urlpatterns = [
    # ex: /ledger/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /ledger/bob/
    url(r'^(?P<pk>[0-9]+)/$', views.FriendView.as_view(), name='friend'),
]
