from django import forms
from .models import Restaurant

class RestaurantForm(forms.ModelForm):
    manager_username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'w-full rounded-lg border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-3 px-4 font-mono',
        'placeholder': 'admin'
    }))
    manager_password = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={
        'class': 'w-full rounded-lg border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-3 px-4 font-mono',
        'placeholder': '••••••••'
    }), required=True)

    class Meta:
        model = Restaurant
        fields = ['name', 'subdomain', 'primary_color', 'secondary_color', 'logo', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full rounded-lg border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-3 px-4'}),
            'subdomain': forms.TextInput(attrs={'class': 'w-full rounded-lg border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-3 px-4 font-mono', 'placeholder': 'e.g. burgerking'}),
            'primary_color': forms.TextInput(attrs={'type': 'color', 'class': 'h-12 w-full cursor-pointer rounded-lg border border-gray-300 shadow-sm'}),
            'secondary_color': forms.TextInput(attrs={'type': 'color', 'class': 'h-12 w-full cursor-pointer rounded-lg border border-gray-300 shadow-sm'}),
            'logo': forms.FileInput(attrs={'class': 'w-full rounded-lg border border-gray-300 shadow-sm py-2 px-3 text-sm'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'h-6 w-6 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'})
        }
