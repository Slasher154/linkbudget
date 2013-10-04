__author__ = 'thanatv'

import sys
import os

from django.http import HttpResponse
from django.shortcuts import render


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
    return render(request, "welcome.html")


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
    return render(request, "progress.html")



def run(command, exit_on_error=True):
    print('\nRunning command: ' + command)
    status = os.system(command)
    if status != 0:
        sys.exit(status)


def django_manage(command):
    run('manage.py ' + command)

