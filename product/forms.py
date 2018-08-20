from django import forms

class UploadFileForm(forms.Form):
    username = forms.CharField(max_length=128)
    price = forms.CharField(max_length=20)
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=300)
    pictures = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
