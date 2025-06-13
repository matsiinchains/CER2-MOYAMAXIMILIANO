from django import forms
from django.contrib.auth.models import User
from .models import SolicitudRetiro

class FormularioRegistroUsuario(forms.ModelForm):
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)
    direccion = forms.CharField(label="Dirección", required=True)
    telefono = forms.CharField(label="Teléfono", required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cd['password2']

class FormularioSolicitud(forms.ModelForm):
    class Meta:
        model = SolicitudRetiro
        fields = ['material', 'cantidad_kg', 'fecha_estimada_retiro']
        widgets = {
            'fecha_estimada_retiro': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'material': forms.Select(attrs={'class': 'form-select'}),
            'cantidad_kg': forms.NumberInput(attrs={'class': 'form-control'}),
        }