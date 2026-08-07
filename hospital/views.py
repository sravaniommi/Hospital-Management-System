from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Doctor,Patient,Appointment

# Create your views here.
def About(request):
    return render(request,'about.html')


def Home(request):
    return render(request, 'home.html')


def Contact(request):
    return render(request,'Contact.html')

def Book_Appointment(request):
    error = ""
    doctor1 = Doctor.objects.all()
    
    if request.method == "POST":
      
            # Retrieve form data
            doctor_name = request.POST['doctor']
            patient_name = request.POST['patient']  # Patient name entered manually
            appointment_date = request.POST['date']
            appointment_time = request.POST['time']
            
            # Check if doctor exists in the system
            doctor = Doctor.objects.filter(name=doctor_name).first()
            
            if doctor:
                # Check if patient exists in the system, or create a new one
                patient = Patient.objects.filter(name=patient_name).first()
                if not patient:
                    # Create a new patient if not found
                    patient = Patient.objects.create(name=patient_name)
                
                # Create the appointment
                Appointment.objects.create(doctor=doctor, patient=patient, date=appointment_date, time=appointment_time)
                error = "no"  # No error means appointment was successfully created
            else:
                error = "Doctor not found"
        
    
    # Pass doctor data and error message to template
    d = {'doctor': doctor1, 'error': error}
    return render(request, 'book_appointment.html', d)


def Index(request):
    if not request.user.is_staff:
       return redirect('login')
    doctors = Doctor.objects.all()
    patient = Patient.objects.all()
    appointment=Appointment.objects.all()
    d=0
    p=0
    a=0
    for i in doctors:
        d+=1
    for i in patient:
        p+=1
    for i in appointment:
        a+=1
    d1={'d':d, 'p':p, 'a':a}
    return render(request, 'index.html', d1)

def Login(request):
    error = ""
    if request.method == "POST":
       u=request.POST['uname']
       p = request.POST['pwd']
       user = authenticate(username= u, password= p)
       try:
           if user.is_staff:
               login(request,user)
               error = "no"

           else:
               error = "yes"

       except:
           error = "yes"
    d = {'error': error}
    return render(request, 'login.html', d)

def Logout_admin(request):
    if not request.user.is_staff:
        return redirect('login')
    
    logout(request)
    return redirect('login')

def View_Doctor(request):
    if not request.user.is_staff:
        return redirect('login')
    doc = Doctor.objects.all()

    d = {'doc': doc}
    return render(request, 'view_doctor.html', d)

def Delete_Doctor(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    return redirect('view_doctor')


def Add_Doctor(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    if request.method == "POST":
       n=request.POST['name']
       m=request.POST['mobile']
       sp=request.POST['special']      
       try:
           Doctor.objects.create(name=n, mobile=m, special=sp)
           error = "no"
       except:
            error = "yes"
    d = {'error': error}
    return render(request, 'add_doctor.html', d)

def View_Patient(request):
    if not request.user.is_staff:
        return redirect('login')
    doc = Patient.objects.all()
    d = {'doc': doc}
    return render(request, 'view_patient.html', d)

def Delete_Patient(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    patient = Patient.objects.get(id=pid)
    patient.delete()
    return redirect('view_patient')


def Add_Patient(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    if request.method == "POST":
       n=request.POST['name']
       g=request.POST['gender']
       m=request.POST['mobile']
       a=request.POST['address']      
       try:
           Patient.objects.create(name=n, gender=g, mobile=m, address=a)
           error = "no"
       except:
            error = "yes"
    d = {'error': error}
    return render(request, 'add_patient.html', d)

def Add_Appointment(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    
    doctor1 = Doctor.objects.all()
    patient1 = Patient.objects.all()
    if request.method == "POST":
       n=request.POST['doctor']
       p=request.POST['patient']
       da=request.POST['date']
       t=request.POST['time'] 
       doctor = Doctor.objects.filter(name=n).first() 
       patient = Patient.objects.filter(name=p).first()
   

       try:
           Appointment.objects.create(doctor=doctor, patient=patient, date=da, time=t)
           error = "no"
       except:
            error = "yes"
    d = {'doctor': doctor1, 'patient': patient1, 'error': error}
    return render(request, 'add_appointment.html', d)


def View_Appointment(request):
    if not request.user.is_staff:
        return redirect('login')
    doc = Appointment.objects.all()
    d = {'doc': doc}
    return render(request, 'view_appointment.html', d)

def Delete_Appointment(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    app = Appointment.objects.get(id=pid)
    app.delete()
    return redirect('view_appointment')