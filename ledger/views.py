from django.views import generic
from django.shortcuts import get_object_or_404,render,reverse
from django.http import HttpResponse,HttpResponseRedirect
from datetime import datetime
from pytz import utc
from django.views.decorators.csrf import csrf_exempt
import requests

from .models import Friend,Entry

def friend_list(request):
    friends = Friend.objects.all()
    # Calculate balances:
    for friend in friends:
        friend.balance = friend.currentBalance()
    return render(request, 'ledger/friend_list.html', {
        'object_list': friends,
    })
    
def entry_list(request, pk):
    entries = Entry.objects.filter(friend=pk)
    for entry in entries:
        entry.this_hash = entry.calcHash()
    return render(request, 'ledger/entry_list.html', {
        'object_list': entries,
    })
    
class FriendDetail(generic.DetailView):
    model = Friend

def inform_friend(friend, entry):
    r = requests.post(friend.contact_url, data = { \
        'secret': friend.secret, \
        'this_hash': entry.calcHash(), \
        'previous_hash': entry.previous_hash, \
        'timestamp': entry.getTimestamp(), \
        'my_new_debt': entry.my_new_debt, \
        'unit_of_value': entry.unit_of_value, \
        'description': entry.description, \
        })
    return True

@csrf_exempt
def webhook(request):
    friend = get_object_or_404(Friend, secret=request.POST['secret'])
    new_entry = Entry.objects.create( \
        date = datetime.fromtimestamp(float(request.POST['timestamp']), utc), \
        friend_id = friend.id,
        previous_hash = request.POST['previous_hash'], \
        # notice minus sign:
        my_new_debt = -float(request.POST['my_new_debt']), \
        description = request.POST['description'], \
        unit_of_value = request.POST['unit_of_value'], \
        )
    new_entry.save()
    return HttpResponse('yes')

def add(request, pk):
    friend = get_object_or_404(Friend, pk = pk)
    last_entry = friend.entry_set.order_by('-date')[0]
    # request.POST['added_debt']
    if (request.POST['unit_of_value'] == last_entry.unit_of_value):
        new_entry = Entry.objects.create( \
            date = datetime.now(), \
            friend_id = friend.id,
            previous_hash = last_entry.calcHash(), \
            my_new_debt = last_entry.my_new_debt \
                + float(request.POST['my_added_debt']), \
            description = 'added through django app', \
            unit_of_value = last_entry.unit_of_value, \
            )
        new_entry.save()
        inform_friend(friend, new_entry)
        # return HttpResponseRedirect(reverse('entry_list', args=(pk,)))
        return HttpResponseRedirect('/ledger/1/')
    else:
        return HttpResponse('no' + pk + last_entry.unit_of_value)
