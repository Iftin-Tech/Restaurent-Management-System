from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem
from apps.menu.models import MenuItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'notes']
        widgets = {
            'table_number': forms.TextInput(attrs={'class': 'border p-2 rounded w-full', 'placeholder': 'Optional'}),
            'notes': forms.Textarea(attrs={'class': 'border p-2 rounded w-full', 'rows': 2, 'placeholder': 'Any special notes?'})
        }

class OrderItemForm(forms.ModelForm):
    menu_item = forms.ModelChoiceField(
        queryset=MenuItem.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'border p-2 rounded w-full'})
    )
    quantity = forms.IntegerField(
        min_value=1, 
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'border p-2 rounded w-full'})
    )
    
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity']

OrderItemFormSet = inlineformset_factory(
    Order, OrderItem, form=OrderItemForm,
    extra=1, can_delete=True
)
