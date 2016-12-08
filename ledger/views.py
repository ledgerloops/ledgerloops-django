from django.views import generic
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse

from .models import Friend,Entry

def calcBalance(entryList):
    total = 0
    for entry in entryList:
      total += entry.my_added_debt
      uov = entry.unit_of_value
    # FIXME: deal with converting multiple uov
    return {
        'amount': total,
        'unit_of_value': uov,
    }

class IndexView(generic.ListView):
    template_name = 'ledger/friend_list.html'
    context_object_name = 'friend_list'
    def get_queryset(self):
        return Friend.objects.all()
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['a'] = {}
        for friend in context['object_list']:
            entryList = Entry.objects.filter(friend=friend.id)
            context['object_list'][friend.id].current_balance = \
               calcBalance(entryList)
        return context


def friend(request, pk):
    f = get_object_or_404(Friend, id=pk)
    template_name = 'ledger/friend.html'
    entryList = Entry.objects.filter(friend=pk)
    return render(request, 'ledger/friend.html', {
      'friend': f,
      'current_balance': calcBalance(entryList),
      'entry_list': entryList,
     })

def add(request, pk):
    return HttpResponse('yes')
