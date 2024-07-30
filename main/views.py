import os
import cv2
import pydicom
import numpy as np
import tensorflow as tf
from django.conf import settings
from .forms import UploadFileFormModel
from django.core.files.storage import default_storage
from django.http import JsonResponse
from .utils import handle_uploaded_file, process_and_predict

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Patient, Bed, Doctor
from .filters import PatientFilter
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# PatientFilter = OrderFilter

model = tf.keras.models.load_model("E:/JOSIAH/AfyaAI_model.h5")

def handle_uploaded_file(f):
    file_path = os.path.join(settings.MEDIA_ROOT, f.name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path

def process_and_predict(filepath):
    try:
        # Load and preprocess the DICOM file
        ds = pydicom.dcmread(filepath)
        image = ds.pixel_array
        image = cv2.resize(image, (50, 50))  # Resize to target size
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)  # Convert to 3 channels
        image = image / 255.0  # Normalize pixel values
        image = np.expand_dims(image, axis=0)  # Model expects a batch dimension

        # Make prediction
        prediction = model.predict(image)
        result = 'Cancer' if prediction[0][0] > 0.5 else 'No Cancer'
        return result
    except Exception as e:
        return f"Error processing the image: {str(e)}"

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileFormModel(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if not file.name.endswith('.dcm'):
                error_message = 'Invalid file format. Please upload a DICOM file.'
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'error': error_message})
                else:
                    return render(request, 'breast_cancer_app/result.html', {'error': error_message})

            file_path = handle_uploaded_file(file)
            prediction = process_and_predict(file_path)
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'prediction': prediction})
            else:
                return render(request, 'breast_cancer_app/result.html', {'prediction': prediction})
    else:
        form = UploadFileForm()
    return render(request, 'breast_cancer_app/upload.html', {'form': form})

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
        else:
            return render(request, 'main/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')




def dashboard(request):
    patients = Patient.objects.all()
    patient_count = patients.count()
    patients_recovered = Patient.objects.filter(status="Recovered")
    patients_deceased = Patient.objects.filter(status="Deceased")
    deceased_count = patients_deceased.count()
    recovered_count = patients_recovered.count()
    beds = Bed.objects.all()
    beds_available = Bed.objects.filter(occupied=False).count()
    ventilators_available = 60  # Example value
    total_ventilators = 100

    ventilator_percentage = (ventilators_available / total_ventilators) * 100
    context = {
        'patient_count': patient_count,
        'recovered_count': recovered_count,
        'beds_available': beds_available,
        'deceased_count':deceased_count,
        'beds':beds,
        'ventilators_available': ventilators_available,
        'total_ventilators': total_ventilators,
        'ventilator_percentage': ventilator_percentage,
    }
    print(patient_count)
    return render(request, 'main/dashboard.html', context)

def add_patient(request):
    beds = Bed.objects.filter(occupied=False)
    doctors = Doctor.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        phone_num = request.POST['phone_num']
        patient_relative_name = request.POST['patient_relative_name']
        patient_relative_contact = request.POST['patient_relative_contact']
        address = request.POST['address']
        symptoms = request.POST.getlist('symptoms')
        prior_ailments = request.POST['prior_ailments']
        bed_num_sent = request.POST['bed_num']
        bed_num = Bed.objects.get(bed_number=bed_num_sent)
        dob = request.POST['dob']
        status = request.POST['status']
        doctor = request.POST['doctor']
        doctor = Doctor.objects.get(name=doctor)
        print(request.POST)
        patient = Patient.objects.create(
            name = name,
        phone_num = phone_num,
        patient_relative_name = patient_relative_name,
        patient_relative_contact = patient_relative_contact, 
        address = address, 
        symptoms = symptoms, 
        prior_ailments = prior_ailments, 
        bed_num = bed_num,
        dob = dob, 
        doctor=doctor,
        status = status
        )
        patient.save()

        bed = Bed.objects.get(bed_number=bed_num_sent)
        bed.occupied = True
        bed.save()
        id = patient.id
        return redirect(f"/patient/{id}")
        
    context = {
        'beds': beds,
        'doctors': doctors
    }
    return render(request, 'main/add_patient.html', context)

def patient(request, pk):
    patient = Patient.objects.get(id=pk)
    if request.method == "POST":
        doctor = request.POST['doctor']
        doctor_time = request.POST['doctor_time']
        doctor_notes = request.POST['doctor_notes']
        mobile = request.POST['mobile']
        mobile2 = request.POST['mobile2']
        relativeName = request.POST['relativeName']
        address  = request.POST['location']
        print(doctor_time)
        print(doctor_notes)
        status = request.POST['status']
        doctor = Doctor.objects.get(name=doctor)
        print(doctor)
        patient.phone_num = mobile
        patient.patient_relative_contact = mobile2
        patient.patient_relative_name = relativeName
        patient.address = address
        patient.doctor = doctor
        patient.doctors_visiting_time = doctor_time
        patient.doctors_notes = doctor_notes
        print(patient.doctors_visiting_time)
        print(patient.doctors_notes)
        patient.status = status
        patient.save()
    context = {
        'patient': patient
    }
    return render(request, 'main/patient.html', context)


def patient_list(request):
    patients = Patient.objects.all()

    # filtering
    myFilter = PatientFilter(request.GET, queryset=patients)

    patients = myFilter.qs
    context = {
        'patients': patients,
        'myFilter': myFilter
    }

    return render(request, 'main/patient_list.html', context)

def patient_view(request):
    return render(request, 'main/patient-view.html')

'''
def autocomplete(request):
    if patient in request.GET:
        name = Patient.objects.filter(name__icontains=request.GET.get(patient))
        name = ['js', 'python']
        
        names = list()
        names.append('Shyren')
        print(names)
        for patient_name in name:
            names.append(patient_name.name)
        return JsonResponse(names, safe=False)
    return render (request, 'main/patient_list.html')
'''

def autosuggest(request):
    query_original = request.GET.get('term')
    queryset = Patient.objects.filter(name__icontains=query_original)
    mylist = []
    mylist += [x.name for x in queryset]
    return JsonResponse(mylist, safe=False)

def autodoctor(request):
    query_original = request.GET.get('term')
    queryset = Doctor.objects.filter(name__icontains=query_original)
    mylist = []
    mylist += [x.name for x in queryset]
    return JsonResponse(mylist, safe=False)

def info(request):
    return render(request, "main/info.html")

def upload(request):
    return render(request, "main/upload.html")
    #itakaa logic ya kufanya image inayokuwa uploaded iwe katika certain preferences such
    #black and white na pia size ya image itakayokuwa uploaded

def dashboard_view(request):
    beds_available = 50  # Replace with actual data retrieval
    total_beds = 100     # Replace with actual data retrieval

    if total_beds != 0:
        bed_percentage = (beds_available / total_beds) * 100
    else:
        bed_percentage = 0

    context = {
        'beds_available': beds_available,
        'total_beds': total_beds,
        'bed_percentage': bed_percentage,
    }

    return render(request, 'main/dashboard.html', context)

