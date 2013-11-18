# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from linkbudget.linkcalc import Link
from linkbudget.models import *
from django.http import HttpResponse


def index(request):
    """
    Link budget input page
    """
    return render(request, "linkbudget/index.html")


def result(request):
    """
    Link budget result page
    """
    mychannel = Channel.objects.filter(name="207-FWD")[0]
    mylink = Link(mychannel, None, 20)
    result = mylink.calculate()

    for m in result.error_messages:
        messages.error(request, m)
    return render(request, "linkbudget/result.html", {"result": result})