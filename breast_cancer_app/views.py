# import os
# import cv2
# import pydicom
# import numpy as np
# from django.conf import settings
# from .breast_forms import UploadFileForm
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# # from .utils import handle_uploaded_file, process_dicom_image

# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# # from .models import Patient, Bed, Doctor
# from django.contrib.auth.models import User, auth
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# import tensorflow as tf
# from tensorflow.keras.models import load_model

# resnetModel = load_model('d:\models\Resnet50_model_cancer-to-be-used-224.keras')
# # PatientFilter = OrderFilter

# # model = tf.keras.models.load_model("E:/JOSIAH/AfyaAI_model.h5")

# def handle_uploaded_file(f):
#     file_path = os.path.join(settings.MEDIA_ROOT, f.name)
#     with open(file_path, 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
#     return file_path

# def process_dicom_image(file_path):
#     try:
#         ds = pydicom.dcmread(file_path)
#         image = ds.pixel_array
        
#         # Normalize pixel values
#         image = (image - np.min(image)) / (np.max(image) - np.min(image))
#         image = (image * 255).astype(np.uint8)
        
#         # Resize and convert to RGB
#         image = cv2.resize(image, (224, 224))  # Adjust size as needed
#         image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        
#         # Normalize for model input
#         image = image / 255.0
        
#         return image
#     except Exception as e:
#         print(f"Error processing DICOM image: {str(e)}")
#         return None

# @csrf_exempt
# def upload_and_predict(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = request.FILES['file']

#             if not file.name.lower().endswith('.dcm'):
#                 error_message = 'Invalid file format. Please upload a DICOM file.'
#                 return JsonResponse({'error': error_message}, status=400)

#             try:
#                 file_path = handle_uploaded_file(file)
#                 img_array = process_dicom_image(file_path)

#                 if img_array is None:
#                     return JsonResponse({'error': 'Error processing the DICOM image'}, status=400)

#                 predictions = resnetModel.predict(np.expand_dims(img_array, axis=0))

#                 cancer_probability = float(predictions[0][0])  # Convert to Python float
#                 predicted_class = "Cancer" if cancer_probability >= 0.5 else "Normal"

#                 calcification_type = get_calcification_type(predictions)

#                 os.remove(file_path)

#                 return JsonResponse({
#                     'predicted_class': predicted_class,
#                     'cancer_probability': cancer_probability,
#                     'calcification_type': calcification_type
#                 })
#             except Exception as e:
#                 return JsonResponse({'error': str(e)}, status=500)
#         else:
#             return JsonResponse({'error': 'Invalid form submission'}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    
#     # else:
#         # form = UploadFileForm()

#     # return render(request, 'main/patient.html', {'form': form})
#     # return JsonResponse({'error': 'Invalid request method'}, status=400)

# def get_calcification_type(predictions):
#     # Provided calcification types dictionary
#     calcification_types = {
#         0: 'No Calcification',
#         1: 'PLEOMORPHIC',
#         2: 'AMORPHOUS',
#         3: 'PUNCTATE',
#         4: 'LUCENT_CENTER',
#         5: 'VASCULAR',
#         6: 'FINE_LINEAR_BRANCHING',
#         7: 'COARSE',
#         8: 'ROUND_AND_REGULAR-LUCENT_CENTER',
#         9: 'PLEOMORPHIC-FINE_LINEAR_BRANCHING',
#         10: 'ROUND_AND_REGULAR-LUCENT_CENTER-PUNCTATE',
#         11: 'ROUND_AND_REGULAR-EGGSHELL',
#         12: 'PUNCTATE-PLEOMORPHIC',
#         13: 'DYSTROPHIC',
#         14: 'LUCENT_CENTERED',
#         15: 'ROUND_AND_REGULAR-LUCENT_CENTER-DYSTROPHIC',
#         16: 'ROUND_AND_REGULAR',
#         17: 'ROUND_AND_REGULAR-LUCENT_CENTERED',
#         18: 'AMORPHOUS-PLEOMORPHIC',
#         19: 'LARGE_RODLIKE-ROUND_AND_REGULAR',
#         20: 'PUNCTATE-AMORPHOUS',
#         21: 'COARSE-ROUND_AND_REGULAR-LUCENT_CENTER',
#         22: 'VASCULAR-COARSE-LUCENT_CENTERED',
#         23: 'LUCENT_CENTER-PUNCTATE',
#         24: 'ROUND_AND_REGULAR-PLEOMORPHIC',
#         25: 'EGGSHELL',
#         26: 'PUNCTATE-FINE_LINEAR_BRANCHING',
#         27: 'VASCULAR-COARSE',
#         28: 'ROUND_AND_REGULAR-PUNCTATE',
#         29: 'SKIN-PUNCTATE-ROUND_AND_REGULAR',
#         30: 'SKIN-PUNCTATE',
#         31: 'COARSE-ROUND_AND_REGULAR-LUCENT_CENTERED',
#         32: 'PUNCTATE-ROUND_AND_REGULAR',
#         33: 'LARGE_RODLIKE',
#         34: 'AMORPHOUS-ROUND_AND_REGULAR',
#         35: 'PUNCTATE-LUCENT_CENTER',
#         36: 'SKIN',
#         37: 'VASCULAR-COARSE-LUCENT_CENTER-ROUND_AND_REGULA',
#         38: 'COARSE-PLEOMORPHIC',
#         39: 'ROUND_AND_REGULAR-PUNCTATE-AMORPHOUS',
#         40: 'COARSE-LUCENT_CENTER',
#         41: 'MILK_OF_CALCIUM',
#         42: 'COARSE-ROUND_AND_REGULAR',
#         43: 'SKIN-COARSE-ROUND_AND_REGULAR',
#         44: 'ROUND_AND_REGULAR-AMORPHOUS',
#         45: 'PLEOMORPHIC-PLEOMORPHIC'
#     }
    
#     # Assuming predictions[0] contains the model's output probabilities
#     # Find the index of the highest probability
#     calcification_index = np.argmax(predictions[0][1:])
    
#     # Return the corresponding calcification type from the dictionary
#     return calcification_types.get(calcification_index, 'Unknown Calcification Type')
