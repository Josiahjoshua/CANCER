from django import forms

class UploadFileFormModel(forms.Form):
    file = forms.FileField()
