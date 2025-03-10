from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Patient, Doctor, AdminProxy, NurseProxy, LabTechProxy, RadiographerProxy, User, Appointment  # Add other models as needed

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
    admin = AdminProxy.objects.get(id=request.user.id)
    appointments = Appointment.objects.all().order_by('-appointment_date')
    
    context = {
        'user': request.user,
        'admin': admin,
        'appointments': appointments,
        'doctors': Doctor.objects.all(),
        'patients': Patient.objects.all()
    }
    return render(request, 'admindash.html', context)

@login_required
def newappointment(request):
    admin = AdminProxy.objects.get(id=request.user.id)
    doctors = Doctor.objects.all()  # if needed for your dynamic dropdown
    context = {
        'admin': admin,
        'doctors': doctors,
    }

    if request.method == "POST":
        # Process the appointment form here.
        # For example, get data from request.POST, validate, and save to an Appointment model (if defined)
        patient_name = request.POST.get('patientName')
        patient_age = request.POST.get('patientAge')
        patient_gender = request.POST.get('patientGender')
        patient_address = request.POST.get('patientAddress')
        phone = request.POST.get('phone')
        appointed_doctor_id = request.POST.get('appointedDoctor')
        print('New appointment form submitted:')
        print(f'patient_name: {patient_name}, patient_age: {patient_age}, patient_gender: {patient_gender}, patient_address: {patient_address}, phone: {phone}, appointed_doctor_id: {appointed_doctor_id}')
        
         # Create a new patient user with role 'patient'
        # Note: In a production system, you may want to generate a random or a more secure temporary password
        new_patient_user = User.objects.create_user(
            phone=phone,
            name=patient_name,
            role='patient',
            password='patient@123'  # Temporary password
        )
        
        # Create the corresponding Patient record
        new_patient = Patient.objects.create(
            user=new_patient_user,
            age=patient_age,
            gender=patient_gender,
            address=patient_address
        )

        # Retrieve the appointed doctor using the selected doctor ID
        try:
            appointed_doctor_user = User.objects.get(id=appointed_doctor_id)
            appointed_doctor = Doctor.objects.get(user=appointed_doctor_user)
        except (User.DoesNotExist, Doctor.DoesNotExist):
            # Handle error appropriately. Here, we simply redirect back with an error message.
            return redirect('admin_dashboard')
        
        # Create the appointment record
        appointment = Appointment.objects.create(
            patient=new_patient,
            doctor=appointed_doctor,
            status='pending'
            # You can add chief_complain, physical_exam, etc. here if your form collects that data.
        )
        print(f'Appointment created with id: {appointment.appointment_id}')
        return redirect('admin_dashboard')
    return render(request, "newappointment.html", context)

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