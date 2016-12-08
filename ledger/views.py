from django.views import generic
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse

from .models import Friend,Entry

def friend_list(request):
    friends = Friend.objects.all()
    # Calculate balances:
    for friend in friends:
        friend.balance = friend.currentBalance()
    return render(request, 'ledger/friend_list.html', {
        'object_list': friends,
    })
    
class FriendDetail(generic.DetailView):
    model = Friend

def add(request, pk):
    return HttpResponse('yes')
