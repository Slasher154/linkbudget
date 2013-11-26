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
    mystring = []
    mychannel = Channel.objects.filter(name="207-FWD")[0]
    mytp = Transponder.objects.filter(name="1G")[0]
    mylink = Link(mychannel, None, 20)
    result = mylink.calculate
    for i in range(-20, 0):
        try:
            ibo = mytp.ibo_at_specific_obo(i)
        except LinkCalcError, e:
            mystring.append("Cannot find IBO at OBO = {0} dB. {1}".format(str(i), e.message))
        else:
            mystring.append("IBO at OBO = {0} dB is {1} dB".format(str(i),str(ibo)))

    for m in result.error_messages:
        messages.error(request, m)
    return render(request, "linkbudget/result.html", {"result": result,
                                                      "mystring": mystring})