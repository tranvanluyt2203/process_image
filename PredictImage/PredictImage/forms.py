# myapp/forms.py
from django import forms

class UploadImageForm(forms.Form):
    image = forms.ImageField(label='Choose an image')
