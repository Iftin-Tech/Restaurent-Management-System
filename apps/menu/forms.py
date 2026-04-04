from django import forms
from .models import MenuCategory, MenuItem

class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = ['name', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border p-2 w-full rounded'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'mt-2'})
        }

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['category', 'name', 'image', 'price', 'is_active']
        widgets = {
            'category': forms.Select(attrs={'class': 'border p-2 w-full rounded'}),
            'name': forms.TextInput(attrs={'class': 'border p-2 w-full rounded'}),
            'image': forms.FileInput(attrs={'class': 'border p-2 w-full rounded'}),
            'price': forms.NumberInput(attrs={'class': 'border p-2 w-full rounded'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'mt-2'})
        }
