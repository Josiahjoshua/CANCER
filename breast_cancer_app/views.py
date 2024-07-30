import os
import pydicom
import numpy as np
import cv2
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from .forms import UploadFileForm
from django.core.files.storage import default_storage
from django.http import JsonResponse
from .utils import handle_uploaded_file, process_and_predict
import tensorflow as tf

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
        form = UploadFileForm(request.POST, request.FILES)
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



# def handle_uploaded_file(f):
#     file_path = os.path.join(settings.MEDIA_ROOT, f.name)
#     with open(file_path, 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
#     return file_path

# def process_and_predict(filepath):
#     # Load and preprocess the DICOM file
#     ds = pydicom.dcmread(filepath)
#     image = ds.pixel_array
#     image = np.expand_dims(image, axis=-1)  # Expand dimensions if needed
#     image = np.expand_dims(image, axis=0)  # Model expects a batch dimension
#     # Make prediction
#     prediction = model.predict(image)
#     # Post-process prediction if necessary (e.g., thresholding, etc.)
#     result = 'Cancer' if prediction[0][0] > 0.5 else 'No Cancer'
#     return result

# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             file_path = handle_uploaded_file(request.FILES['file'])
#             prediction = process_and_predict(file_path)
            
#             if request.is_ajax():
#                 return JsonResponse({'prediction': prediction})
#             else:
#                 return render(request, 'breast_cancer_app/result.html', {'prediction': prediction})
#     else:
#         form = UploadFileForm()
#     return render(request, 'breast_cancer_app/upload.html', {'form': form})
