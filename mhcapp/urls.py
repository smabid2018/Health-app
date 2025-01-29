from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("drloa", views.drloa, name="drloa"),
    path("loa", views.loa, name="drloa"),
    path("admindash", views.admindash, name="admindash"),
    path("nursedash", views.nursedash, name="nursedash"),
    path("vitalsentry", views.vitalsentry, name="vitalsentry"),
    path("patientsform", views.patientsform, name="patientsform"),

]