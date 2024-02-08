from django import forms
from .models import vendor


class vendorform(forms.ModelForm):
    class Meta:
        model = vendor
        fields = ['vandor_name' , 'vendor_license']