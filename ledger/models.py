from __future__ import unicode_literals

from django.db import models
from hashlib import sha256
import json
from datetime import datetime

class Friend(models.Model):
    nick = models.CharField(max_length=20)
    def currentBalance(self):
        # last_entry = self.entry_set.reverse()[0]
        last_entry = self.entry_set.all()[1] # FIXME: how can I get the length of entry_set? why is reverse() not doing what I expect it to?
        return str(last_entry.my_new_debt) + ' ' + last_entry.unit_of_value
    def __str__(self):
        return '(' + self.nick + ')'

class Entry(models.Model):
    description = models.CharField(max_length=200)
    previous_hash = models.CharField(max_length=200)
    date = models.DateTimeField('date')
    my_new_debt = models.IntegerField(default=0)
    unit_of_value = models.CharField(max_length=10)
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)
    def calcHash(self):
        utc_naive  = self.date.replace(tzinfo=None) - self.date.utcoffset()
        timestamp = (utc_naive - datetime(1970, 1, 1)).total_seconds()
        stringified = json.dumps({
            "previous_hash": self.previous_hash,
            "my_new_debt": self.my_new_debt,
            "unit_of_value": self.unit_of_value,
            "timestamp": timestamp,
        })
        return sha256(stringified.encode('utf-8')).hexdigest()
        # return stringified.encode('utf-8')
    def __str__(self):
        return '(' + self.friend.nick + ')' \
            + self.description \
            + ': ' + str(self.my_new_debt) \
            + self.unit_of_value
