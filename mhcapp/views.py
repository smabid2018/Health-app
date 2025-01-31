from django.shortcuts import render, HttpResponse

# Create your views here.

def home(request):
    return render(request, "drdash.html")

def drloa(request):
    return render(request, "drLOA.html")


def loa(request):
    return render(request, "loa.html")


def admindash(request):
    return render(request, "admindash.html")

def nursedash(request):
    return render(request, "nursedash.html")

def vitalsentry(request):
    return render(request, "vitalsentry.html")

def patientsform(request):
    return render(request, "patientsform.html")

def radiographerdash(request):
    return render(request, "radiographerdash.html")

def techdash(request):
    return render(request, "techdash.html")

def radnewreq(request):
    return render(request, "radnewreq.html")
