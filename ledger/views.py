from django.views import generic
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse

from .models import Friend,Entry

class FriendList(generic.ListView):
    model = Friend
    
class FriendDetail(generic.DetailView):
    model = Friend
    def get_object(self):
        friend = super(FriendDetail, self).get_object()
        context['current_balance'] = self.friend.currentBalance()
        return context

def add(request, pk):
    return HttpResponse('yes')
