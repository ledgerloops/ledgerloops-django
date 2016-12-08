from __future__ import unicode_literals

from django.db import models


class Entry(models.Model):
    description = models.CharField(max_length=200)
    date = models.DateTimeField('date')
    amount = models.IntegerField(default=0)
    unit_of_value = models.CharField(max_length=10)
    def __str__(self):
        return self.description

class Balance(models.Model):
    last_entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    # this_hash is hash(last_hash + stringify(last_entry))
    this_hash = models.CharField(max_length=20)
    # last_hash is null for first ledger balance
    last_hash = models.CharField(max_length=20)
    debtor = models.CharField(max_length=20)
    amount = models.IntegerField(default=0)
    unit_of_value = models.CharField(max_length=10)
    def __str__(self):
        return self.amount
