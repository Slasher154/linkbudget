__author__ = 'thanatv'

from django.http import HttpResponse
import sys
import os
import os.path
ABSOLUTE_PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

def index(request):
    """
    Display welcome message.
    :param request:
    :return:
    """
    str = ""
    print(ABSOLUTE_PROJECT_DIR)
    print(os.path.dirname(__file__))
    print(os.path.abspath(os.path.dirname(__file__)))
    print(os.path.join(ABSOLUTE_PROJECT_DIR, 'static'))
    return HttpResponse("Hello World")


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

def run(command, exit_on_error=True):
    print('\nRunning command: '+command)
    status = os.system(command)
    if status != 0:
        sys.exit(status)


def django_manage(command):
    run('manage.py ' + command)