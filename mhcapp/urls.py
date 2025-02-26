from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("drloa/", views.drloa, name="drloa"),
    path("loa/", views.loa, name="drloa"),
    path("admindash/", views.admindash, name="admindash"),
    path("nursedash/", views.nursedash, name="nursedash"),
    path("vitalsentry/", views.vitalsentry, name="vitalsentry"),
    path("patientsform/", views.patientsform, name="patientsform"),
    path("radiographerdash/", views.radiographerdash, name="radiographerdash"),
    path("techdash/", views.techdash, name="techdash"),
    path("radnewreq/", views.radnewreq, name="radnewreq"),
    path("patient_dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path("login/", views.login_view, name="login"),
    path("techreqdetails/", views.techreqdetails, name="techreqdetails"),
]
