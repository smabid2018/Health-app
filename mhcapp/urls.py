from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("login/", views.login_view, name="login"),

    #path("", views.home, name="home"),

    path("drloa/", views.drloa, name="drloa"),
    path("loa/", views.loa, name="drloa"),


    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("newappointment/", views.newappointment, name="newappointment"),

    
    path("nursedash/", views.nursedash, name="nursedash"),
    path("vitalsentry/", views.vitalsentry, name="vitalsentry"),
    
    path("radiographerdash/", views.radiographerdash, name="radiographerdash"),
    path("techdash/", views.techdash, name="techdash"),
    path("radnewreq/", views.radnewreq, name="radnewreq"),
    path("patient_dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path("techreqdetails/", views.techreqdetails, name="techreqdetails"),
]
