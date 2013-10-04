from django.db import models

# Create your models here.


class Progress(models.Model):
    """
    Store the progress of link budget website project
    """
    week = models.IntegerField()
    actions = models.CharField()
    status = models.CharField(
        ('In progress', 'In progress'),
        ('Not started', 'Not started'),
        ('Behind Schedule', 'Behind Schedule'),
        ('Completed', 'Completed'),
    )
    remarks = models.CharField()