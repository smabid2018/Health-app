from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Patient, Doctor, AdminProxy, NurseProxy, LabTechProxy, RadiographerProxy # Add other models as needed

# Create your views here.

def home(request):
    return render(request, "drdash.html")

def drloa(request):
    return render(request, "drLOA.html")

def loa(request):
    return render(request, "loa.html")

# def admindash(request):
#     return render(request, "admindash.html")



def vitalsentry(request):
    return render(request, "vitalsentry.html")

def patientsform(request):
    return render(request, "patientsform.html")

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

@login_required
def nursedash(request):
    nurse = NurseProxy.objects.get(id=request.user.id)
    context = {
        'user': request.user,
        'nurse': nurse,
        'patients': Patient.objects.all()
    }
    return render(request, "nursedash.html", context)

@login_required
def techdash(request):
    labtech = LabTechProxy.objects.get(id=request.user.id)
    context = {
        'user': request.user,
        'labtech': labtech,
        # 'techreqs': TechReq.objects.all()
    }
    return render(request, "techdash.html", context)

@login_required
def radiographerdash(request):
    rg = RadiographerProxy.objects.get(id=request.user.id)
    context = {
        'user': request.user,
        'rg': rg,
        # 'radreqs': RadReq.objects.all()
    }
    return render(request, "radiographerdash.html", context)

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
            elif user.role == 'nurse':
                print(f'user detected: {user.role}, redirecting to nursedash...')
                return redirect('nursedash')
            elif user.role == 'labt':
                print(f'user detected: {user.role}, redirecting to techdash...')
                return redirect('techdash')
            elif user.role == 'rg':
                print(f'user detected: {user.role}, redirecting to radiographerdash...')
                return redirect('radiographerdash')

            # Add other roles as needed
        else:
            messages.error(request, 'Invalid phone number or password')
    
    return render(request, 'login.html')