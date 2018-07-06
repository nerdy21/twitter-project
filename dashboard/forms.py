from django import forms

class InputForm(forms.Form):
    user_id = forms.CharField()