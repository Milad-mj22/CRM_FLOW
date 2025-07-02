# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Driver, CarModel

class DriverRegisterForm(forms.ModelForm):
    username = forms.CharField(label="نام کاربری", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(label="نام کامل", widget=forms.TextInput(attrs={'class': 'form-control'}))
    national_code = forms.CharField(label="کد ملی", widget=forms.TextInput(attrs={'class': 'form-control'}))
    car_model = forms.ModelChoiceField(queryset=CarModel.objects.all(), label="مدل خودرو", widget=forms.Select(attrs={'class': 'form-control'}))
    license_plate = forms.CharField(label="شماره پلاک", widget=forms.TextInput(attrs={'class': 'form-control'}))
    car_code = forms.CharField(label="کد خودرو", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Driver
        fields = ['full_name', 'national_code', 'car_model', 'license_plate', 'car_code']

    def save(self, commit=True):
        # ابتدا یوزر ساخته می‌شود
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        # سپس راننده به یوزر نسبت داده می‌شود
        driver = super().save(commit=False)
        driver.user = user
        if commit:
            driver.save()
        return driver
