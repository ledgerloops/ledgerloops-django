from __future__ import unicode_literals

from django.db import models

class Friend(models.Model):
    nick = models.CharField(max_length=20)
    def __str__(self):
        return '(' + self.nick + ')'

class Entry(models.Model):
    description = models.CharField(max_length=200)
    date = models.DateTimeField('date')
    my_added_debt = models.IntegerField(default=0)
    unit_of_value = models.CharField(max_length=10)
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)
    def __str__(self):
        return '(' + self.friend.nick + ')' \
            + self.description \
            + ': ' + str(self.my_added_debt) \
            + self.unit_of_value
