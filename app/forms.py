from django import forms

class SettingForm(forms.Form):
    news = forms.CharField(label='news')
    stock = forms.CharField(label='stock')
    weather = forms.CharField(label='weather')
    mail = forms.CharField(label='mail')
    calendar = forms.CharField(label='calendar')