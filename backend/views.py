from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse


def index(request):
    with open("/Users/caishichao/Code/sign/action.log") as f:
        result = f.readlines()[-10:-1]
    return HttpResponse(result)