
from django.contrib.auth import authenticate

from .models import User
from django import forms



class UserRegisterForm(forms.ModelForm):
    # Opciones para el tipo de usuario (limitadas a profesor y conserje)
    TIPO_USUARIO_CHOICES = [
        ('profesor', 'Profesor'),
        ('conserje', 'Conserje'),
    ]

    # Primer campo de contraseña
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(  # Campo tipo password (oculta caracteres)
            attrs={
                'placeholder': 'Contraseña',
                'class': 'form-control',
            }
        )
    )

    # Segundo campo de contraseña (para confirmar)
    password2 = forms.CharField(
        label='Repetir Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir Contraseña',
                'class': 'form-control',
            }
        )
    )

    # Campo para seleccionar tipo de usuario
    type_user = forms.ChoiceField(
        label='Tipo de Usuario',
        choices=TIPO_USUARIO_CHOICES,  # Usa las opciones definidas arriba
        initial='profesor',  # Valor por defecto
        widget=forms.Select(attrs={'class': 'form-select'})  # Estilizado
    )

    # Define qué modelo representa este formulario y qué campos usará
    class Meta:
        model = User  # Se asume que `User` es un modelo personalizado
        fields = ('email', 'nombre', 'apellido')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Correo Electrónico', 'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Apellido', 'class': 'form-control'}),
        }

    # Validación para asegurarse que las dos contraseñas coincidan
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden')
        return password2





class LoginForm(forms.Form):
    # Campo de email
    email = forms.CharField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
    )

    # Campo de contraseña
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'form-control'}),
    )

    # Constructor personalizado que agrega una clase CSS si hay errores
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Recorre todos los campos y agrega la clase 'is-invalid' si el campo tiene errores
        for field_name, field in self.fields.items():
            css_class = field.widget.attrs.get('class', '')
            if self.errors.get(field_name):
                field.widget.attrs['class'] = css_class + ' is-invalid'

    # Validación global del formulario
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # Si hay email y contraseña, intenta autenticar al usuario
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                # Si no se pudo autenticar, lanza un error general del formulario
                raise forms.ValidationError('Los datos no son correctos')
        return cleaned_data
