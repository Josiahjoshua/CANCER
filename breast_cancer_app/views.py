import os
import pydicom
import numpy as np
import tensorflow as tf
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from django.core.files.storage import default_storage
from django.http import JsonResponse
from .utils import handle_uploaded_file, process_and_predict

# Load your trained model
# model = tf.keras.models.load_model('path/to/my/trained_model.h5')

def handle_uploaded_file(f):
    file_path = os.path.join(settings.MEDIA_ROOT, f.name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path

def process_and_predict(filepath):
    # Load and preprocess the DICOM file
    ds = pydicom.dcmread(filepath)
    image = ds.pixel_array
    image = np.expand_dims(image, axis=-1)  # Expand dimensions if needed
    image = np.expand_dims(image, axis=0)  # Model expects a batch dimension
    # Make prediction
    prediction = model.predict(image)
    # Post-process prediction if necessary (e.g., thresholding, etc.)
    result = 'Cancer' if prediction[0][0] > 0.5 else 'No Cancer'
    return result

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_path = handle_uploaded_file(request.FILES['file'])
            prediction = process_and_predict(file_path)
            
            if request.is_ajax():
                return JsonResponse({'prediction': prediction})
            else:
                return render(request, 'breast_cancer_app/result.html', {'prediction': prediction})
    else:
        form = UploadFileForm()
    return render(request, 'breast_cancer_app/upload.html', {'form': form})
