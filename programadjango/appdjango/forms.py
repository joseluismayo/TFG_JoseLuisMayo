from django import forms
from django.core.validators import RegexValidator

#creacion del formulario del login para que el usuario pueda iniciar sesion
class LoginFormulario(forms.Form):
    correo = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu correo electrónico'})
    )
    contrasena = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Tu contraseña'})
    )

#creacion del formulario de registro para que el usuario pueda registrar una cuenta en la base de datos
class RegistroFormulario(forms.Form):
    nombre = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'})
    )
    correo = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@gmail.com'})
    )
    contrasena = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Tu contraseña'}),
        validators=[RegexValidator(
            regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$',
            message="La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número."
        )]
    )
    
    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')
        return contrasena







