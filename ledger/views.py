from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Entry,Balance,Friend

class IndexView(generic.ListView):
    template_name = 'ledger/index.html'
    context_object_name = 'friend_list'
    def get_queryset(self):
        return Friend.objects.all()

class FriendView(generic.DetailView):
    model = Friend
    template_name = 'ledger/friend.html'
