from __future__ import unicode_literals

from django.db import models
from hashlib import sha256
import json
from datetime import datetime

class Friend(models.Model):
    nick = models.CharField(max_length=20)
    contact_url = models.CharField(max_length=200)
    secret = models.CharField(max_length=40)
    def currentBalance(self):
        last_entry = self.entry_set.order_by('id')[0]
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
    def getTimestamp(self):
        return self.date.timestamp()
        # if (type(self.date.utcoffset) == 'NoneType'):
        #     utc_naive  = self.date.replace(tzinfo=None)
        # else:
        #     utc_naive  = self.date.replace(tzinfo=None) - self.date.utcoffset()
        # return (utc_naive - datetime(1970, 1, 1)).total_seconds()
    def calcHash(self):
        stringified = json.dumps({
            "previous_hash": self.previous_hash,
            "my_new_debt": self.my_new_debt,
            "unit_of_value": self.unit_of_value,
            "timestamp": self.getTimestamp(),
        })
        return sha256(stringified.encode('utf-8')).hexdigest()
    def __str__(self):
        return '(' + self.friend.nick + ')' \
            + self.description \
            + ': ' + str(self.my_new_debt) \
            + self.unit_of_value
