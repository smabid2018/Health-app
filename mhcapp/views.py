from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Patient, Doctor, AdminProxy# Add other models as needed

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


@login_required
def patient_dashboard(request):
    try:
        patient = Patient.objects.get(user=request.user)
        context = {
            'user': request.user,
            'patient': patient,
            # 'appointments': patient.appointment_set.all(),
            # 'medical_records': patient.medicalrecord_set.all()
        }
        return render(request, 'patientdash.html', context)
    except Patient.DoesNotExist:
        messages.error(request, 'Patient profile not found')
        return redirect('login')
    except Exception as e:
        messages.error(request, f'Error accessing dashboard: {str(e)}')
        return redirect('home')

def techreqdetails(request):
    return render(request, "techreqdetails.html")

@login_required
def doctor_dashboard(request):
    doctor = Doctor.objects.get(user=request.user)
    context = {
        'user': request.user,
        'doctor': doctor,
        # 'upcoming_appointments': doctor.appointment_set.filter(status='scheduled'),
        # 'patients': doctor.patients.all()
    }
    return render(request, 'drdash.html', context)

@login_required
def admin_dashboard(request):
    admin = AdminProxy.objects.get(id=request.user.id)
    context = {
        'user': request.user,
        'admin': admin,
        'doctors': Doctor.objects.all(),
        'patients': Patient.objects.all()
    }
    return render(request, 'admindash.html', context)

def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        print(f'phone: {phone}, password: {password}')
        
        # Authenticate using phone as username (since we're using phone for auth)
        user = authenticate(request, username=phone, password=password)  # Changed parameter
        print(f'user: {user}')
        
        if user is not None:
            print(f'user detected: {user.role}, logging in...')
            login(request, user)
            
            # Redirect based on role
            if user.role == 'patient':
                print(f'user detected: {user.role}, redirecting to patient_dashboard...')
                return redirect('patient_dashboard')
            elif user.role == 'doctor':
                print(f'user detected: {user.role}, redirecting to doctor_dashboard...')
                return redirect('doctor_dashboard')
            elif user.role == 'admin':
                print(f'user detected: {user.role}, redirecting to admin_dashboard...')
                return redirect('admin_dashboard')
            # Add other roles as needed
        else:
            messages.error(request, 'Invalid phone number or password')
    
    return render(request, 'login.html')