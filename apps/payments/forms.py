from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['method', 'amount_paid']
        widgets = {
            'method': forms.Select(attrs={'class': 'border border-gray-300 p-3 rounded w-full text-lg shadow-sm focus:ring-blue-500 focus:border-blue-500'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'border border-gray-300 p-3 rounded w-full text-lg font-bold text-green-700 bg-gray-50 focus:ring-blue-500 focus:border-blue-500'})
        }
