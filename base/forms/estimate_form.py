from django import forms
from base.models import Estimate, EstimateLine

class EstimateCreateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = [
            'project',
            'cost_estimate',
            'estimate_number',
            'title',
            'quote_date',
            'expiration_date',
            'tax_rate',
            'note',
        ]

        widgets = {
          'project': forms.Select(attrs={'class': 'form-select',}),
          'cost_estimate': forms.Select(attrs={'class': 'form-select',}),
          'estimate_number': forms.TextInput(attrs={'class': 'form-control',}),
          'title': forms.TextInput(attrs={'class': 'form-control',}),
          'quote_date': forms.DateInput(attrs={'class': 'form-control','type': 'date',}),
          'expiration_date': forms.DateInput(attrs={'class': 'form-control','type': 'date',}),
          'tax_rate': forms.NumberInput(attrs={'class': 'form-control','step': '1','min': '0',}),
          'note': forms.Textarea(attrs={'class': 'form-control','rows': 4,}),
        }

class EstimateUpdateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = [
            'project',
            'title',
            'cost_estimate',
            'estimate_number',
            'quote_date',
            'expiration_date',
            'status',
            'tax_rate',
            'note',
        ]

        widgets = {
          'project': forms.Select(attrs={'class': 'form-select',}),
          'cost_estimate': forms.Select(attrs={'class': 'form-select',}),
          'estimate_number': forms.TextInput(attrs={'class': 'form-control',}),
          'title': forms.TextInput(attrs={'class': 'form-control',}),
          'quote_date': forms.DateInput(attrs={'class': 'form-control','type': 'date',}),
          'expiration_date': forms.DateInput(attrs={'class': 'form-control','type': 'date',}),
          'status': forms.Select(attrs={'class': 'form-select',}),
          'tax_rate': forms.NumberInput(attrs={'class': 'form-control','step': '1','min': '0',}),
          'note': forms.Textarea(attrs={'class': 'form-control','rows': 4,}),
        }

class EstimateLineForm(forms.ModelForm):
    class Meta:
        model = EstimateLine
        fields = [
            'item_name',
            'quantity',
            'unit',
            'unit_price',
        ]

        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control',}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1',}),
            'unit': forms.TextInput(attrs={'class': 'form-control',}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '1',}),
        }