from django import forms
from .models import SignupCode

class SignupCodeForm(forms.ModelForm):
    class Meta:
        model = SignupCode
        fields = ('email', )

class SignupCodeUpdateForm(forms.ModelForm):
    class Meta:
        model = SignupCode
        fields = ('email', 'authorization_code', )
        widgets = {
            # 'email': forms.EmailInput(attrs={'readonly': True}),
            'authorization_code': forms.TextInput(attrs={'readonly': True})
        }
