from django.views import generic
from django.shortcuts import get_object_or_404,render,reverse
from django.http import HttpResponse,HttpResponseRedirect
from datetime import datetime

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
        # return HttpResponseRedirect(reverse('entry_list', args=(pk,)))
        return HttpResponseRedirect('/ledger/1/')
    else:
        return HttpResponse('no' + pk + last_entry.unit_of_value)
