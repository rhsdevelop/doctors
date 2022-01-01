from django import forms
from .models import Doctor, Phone, Specialty


class AddSpecialtyForm(forms.ModelForm):
    class Meta:
        model = Specialty
        exclude = ['id', 'register_date']


class FindSpecialtyForm(forms.ModelForm):
    class Meta:
        model = Specialty
        fields = ['name']


class AddDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude = ['id',]


class FindDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialty', 'hospital', 'city']


class AddPhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        exclude = ['id', 'doctor']
