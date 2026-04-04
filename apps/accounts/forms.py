from django import forms
from .models import User, Role, UserRole

class CustomUserCreationForm(forms.ModelForm):
    full_name = forms.CharField(max_length=150, required=True, 
                                widget=forms.TextInput(attrs={'placeholder': 'Enter full name', 'class': 'form-input-premium'}))
    username = forms.CharField(max_length=150, required=True, 
                                widget=forms.TextInput(attrs={'placeholder': 'username', 'class': 'form-input-premium'}))
    email = forms.EmailField(required=True, 
                             widget=forms.EmailInput(attrs={'placeholder': 'email@example.com', 'class': 'form-input-premium'}))
    phone_number = forms.CharField(max_length=20, required=False, 
                                   widget=forms.TextInput(attrs={'placeholder': '+252...', 'class': 'form-input-premium'}))
    
    # 🚨 Password Input (Explicitly visible and editable for admin)
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': '........', 'class': 'form-input-premium'})
    )
    
    # 🚨 Role Selection as a Dropdown
    role = forms.ModelChoiceField(
        queryset=Role.objects.none(), 
        required=True,
        empty_label="-- Select Role --",
        widget=forms.Select(attrs={'class': 'form-select-premium'})
    )
    
    is_active = forms.BooleanField(initial=True, required=False)
    
    class Meta:
        model = User
        fields = ('full_name', 'username', 'email', 'phone_number', 'password', 'is_active')

    def __init__(self, *args, **kwargs):
        using_db = kwargs.pop('using_db', 'default')
        super().__init__(*args, **kwargs)
        self.fields['role'].queryset = Role.objects.using(using_db).all()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.full_name = self.cleaned_data['full_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.email = self.cleaned_data['email']
        user.is_active = self.cleaned_data['is_active']
        
        if commit:
            user.save()
            # Clear old and apply SINGLE selected role
            UserRole.objects.filter(user=user).delete()
            selected_role = self.cleaned_data['role']
            UserRole.objects.create(user=user, role=selected_role)
        return user
