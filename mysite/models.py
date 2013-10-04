__author__ = 'thanatv'

from django.db import models

# Create your models here.


class Progress(models.Model):
    """
    Store the progress of link budget website project
    """
    week = models.IntegerField()
    actions = models.CharField(max_length=300)
    percent = models.IntegerField()
    status = models.CharField(max_length=40)
    remarks = models.CharField(max_length=300)

    def __str__(self):
        return self.actions

    class Meta:
        ordering = ['week']