from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField



class VinForm(forms.Form):
   
    vin = forms.CharField(label='VIN/FRAME-код', max_length=100) 

    captcha = ReCaptchaField()
    vin.widget.attrs.update({'class': 'block__input', 'placeholder': 'VIN/FRAME-код'})