from django import forms
from base.models import CostEstimate, CostEstimateLine

class CostEstimateForm(forms.ModelForm):
    class Meta:
        model = CostEstimate
        fields = [
            'project',
            'title',
            'vendor_name',
            'quote_date',
            'expiration_date',
            'tax_rate',
            'pdf_file',
            'note',
        ]

        widgets = {
          'project': forms.Select(attrs={'class': 'form-select',}),
          'title': forms.TextInput(attrs={'class': 'form-control',}),
          'vendor_name': forms.TextInput(attrs={'class': 'form-control',}),
          'quote_date': forms.DateInput(attrs={'class': 'form-control','type': 'date',}),
          'expiration_date': forms.DateInput(attrs={'class': 'form-control','type': 'date',}),
          'tax_rate': forms.NumberInput(attrs={'class': 'form-control','step': '1','min': '0',}),
          'pdf_file': forms.ClearableFileInput(attrs={'class': 'form-control',}),
          'note': forms.Textarea(attrs={'class': 'form-control','rows': 4,}),
        }

class CostEstimateLineForm(forms.ModelForm):
    class Meta:
        model = CostEstimateLine
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