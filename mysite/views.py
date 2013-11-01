__author__ = 'thanatv'

import sys
import os
import json
from mysite.models import Progress, Parent

from django.http import HttpResponse
from django.shortcuts import render
from datetime import date, timedelta
from django.core import serializers
from custom_functions import JSONSerializer


ABSOLUTE_PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def index(request):
    """
    Display welcome message.
    :param request:
    :return:
    """
    print(ABSOLUTE_PROJECT_DIR)
    for i in range(0, 5):
        num = i * 20

    print(os.path.dirname(__file__))
    print(os.path.abspath(os.path.dirname(__file__)))
    print(os.path.join(ABSOLUTE_PROJECT_DIR, 'static'))
    return HttpResponse("Hello World")


def welcome(request):
    """
    A Welcome page
    """
    return render(request, 'welcome.html')


def deploy(request):
    """
    A webpage to invoke manage.py commands
    """
    os.chdir(ABSOLUTE_PROJECT_DIR)

    # install requirements to local folder
    #run('pip install --requirement=requirements.txt')

    # run manage.py syncdb --noinput
    #django_manage('syncdb --noinput')

    # run manage.py migrate
    #django_manage('migrate')

    # collect static
    django_manage('collectstatic --noinput')

    # that's all
    print "Bye!"
    return HttpResponse("Deployment finished")


def progress(request):
    """A project progress page"""
    progresses = Progress.objects.all()
    start_date = date(2013, 9, 30)
    start_date_list = []
    stop_date_list = []
    for p in progresses:
        start_date_list.append(start_date + timedelta(weeks=p.week - 1))
        stop_date_list.append(start_date + timedelta(weeks=p.week - 1, days=4))
    progresses_with_dates = zip(progresses, start_date_list, stop_date_list)
    return render(request, 'progress.html',
                  {"progresses": progresses_with_dates})


def testjson(request):
    #data = serializers.serialize("json", Progress.objects.all())
    #data = json.dumps(Progress.objects.all())
    serializer = JSONSerializer()
    data1 = serializer.serialize(Progress.objects.all())
    qset = Parent.objects.select_related()
    data2 = serializer.serialize(qset)
    return render(request, 'testjson.html', {"data1": data1, "data2": data2})


def run(command, exit_on_error=True):
    print('\nRunning command: ' + command)
    status = os.system(command)
    if status != 0:
        sys.exit(status)


def django_manage(command):
    run('manage.py ' + command)


class Parents:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Children:
    def __init__(self, name, age, parent):
        self.name = name,
        self.age = age
        self.parent = parent