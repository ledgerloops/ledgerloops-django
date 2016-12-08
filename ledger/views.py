from django.shortcuts import render,get_object_or_404

from .models import Entry,Balance,Friend

def friendEntry(f):
    b = f.current_balance
    return '<a href="./'+f.nick+'">'+f.nick+'</a>:' + str(b.amount) + ' ' \
        + b.unit_of_value

def ledgerEntry(e):
    return ' '.join([e.description, str(e.amount), e.unit_of_value])

def index(request):
    return render(request, 'ledger/index.html', {
      'friend_list': Friend.objects.all(),
    })

def friend(request, friend_id):
    friend = get_object_or_404(Friend, nick=friend_id)
    balance = friend.current_balance
    entry = balance.last_entry
    return render(request, 'ledger/friend.html', {
        'friend': friend,
        'balance': balance,
        'entry': entry,
    })
