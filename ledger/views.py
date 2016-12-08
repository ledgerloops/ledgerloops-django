from django.shortcuts import render
from django.http import HttpResponse
from .models import Entry,Balance,Friend

def friendEntry(f):
    b = f.current_balance
    balance = str(b.amount) + ' ' + b.unit_of_value
    return '<a href="./'+f.nick+'">'+f.nick+'</a>:'+balance

def ledgerEntry(e):
    return ' '.join([e.description, str(e.amount), e.unit_of_value])

def index(request):
    friends = Friend.objects.all()
    output = ', '.join([friendEntry(f) for f in friends])
    return HttpResponse(output)

def friend(request, friend_id):
    f = Friend.objects.get(nick=friend_id)
    e = f.current_balance.last_entry
    return HttpResponse('<br>'.join([ \
        'You\'re looking at the ledger for friend %s.' % friend_id \
            + '(<a href="../">back</a>)', \
        friendEntry(f), \
        'Last entry:' + ledgerEntry(e) ]))
