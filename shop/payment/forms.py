from django import forms
from .models import Customer, ShippingAddress


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control mt-2 mb-4 ps-3'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control mt-2 mb-4 ps-3'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control mt-2 mb-4 ps-3'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control mt-2 mb-4 ps-3'
            })
        }
        labels = {
            'first_name': 'First Name*',
            'last_name': 'Last Name*',
            'phone': 'Phone *',
            'email': 'Email address *'
        }


class ShippingForm(forms.ModelForm):
    name_company = forms.CharField(label='Company Name(optional)*', required=True, widget=forms.TextInput(attrs={
        'class': 'form-control mt-3 ps-3 mb-4'
    }))

    order_notes = forms.CharField(label='Order notes (optional)', required=True, widget=forms.TextInput(attrs={
        'class': 'form-control mt-3 ps-3 mb-4'
    }))

    class Meta:
        model = ShippingAddress
        fields = [
            'name_company',
            'city_or_region',
            'address_part_one',
            'address_part_two',
            'town_city',
            'state',
            'zip_code',
            'order_notes'
        ]
        widgets = {
            'city_or_region': forms.Select(attrs={
                'class': 'form-select form-control mt-2 mb-4'
            }),
            'address_part_one': forms.TextInput(attrs={
                'class': 'form-control mt-3 ps-3 mb-4'
            }),
            'address_part_two': forms.TextInput(attrs={
                'class': 'form-control mt-2 mb-4'
            }),
            'town_city': forms.TextInput(attrs={
                'class': 'form-control mt-2 mb-4'
            }),
            'state': forms.Select(attrs={
                'class': 'form-select form-control mt-2 mb-4'
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'form-control mt-2 mb-4'
            })
        }
        labels = {
            'city_or_region': 'Country / Region*',
            'address_part_one': 'House number and street name',
            'address_part_two': 'Appartments, suite, etc.',
            'town_city': 'Town / City *',
            'state': 'State *',
            'zip_code': 'Zip Code *',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city_or_region'].widget.choices = list(self.fields['city_or_region'].widget.choices)
        self.fields['city_or_region'].widget.choices.pop(0)

        self.fields['state'].widget.choices = list(self.fields['state'].widget.choices)
        self.fields['state'].widget.choices.pop(0)
