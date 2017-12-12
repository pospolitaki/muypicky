from django import forms
from .models import RestaurantLocation
from .validators import validate_category

class RestaurantCreateForm(forms.Form):
    name        = forms.CharField()
    location    = forms.CharField(required=False)
    category    = forms.CharField(required=False)

def clean_name(self):
    name = self.cleaned_data.get('name')
    if name == 'Hallo':
        raise forms.ValidationError('Not calid name')
    return name

# def clean_email(self):
#     email = self.cleaned_data.get('name')
#     if 'edu' in email:
#         raise forms.ValidationError('we do not accept edu emails')
#     return email

class RestaurantLocationCreateForm(forms.ModelForm):
    #email       = forms.EmailField()
    #category = forms.CharField(required = False, validators = [validate_category])
    class Meta:
        model = RestaurantLocation
        fields = [
            'name', 
            'location',
            'category',
            'slug'
        ]

