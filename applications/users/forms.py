from django import forms
from django.contrib.auth import authenticate

from .models import User
from django import forms
from django.contrib.auth import get_user_model


class UserRegisterForm(forms.ModelForm):
    TIPO_USUARIO_CHOICES = [
        ('profesor', 'Profesor'),
        ('conserje', 'Conserje'),
    ]

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class': 'form-control',
            }
        )
    )

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

    type_user = forms.ChoiceField(
        label='Tipo de Usuario',
        choices=TIPO_USUARIO_CHOICES,
        initial='profesor',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ('email', 'nombre', 'apellido')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Correo Electrónico', 'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Apellido', 'class': 'form-control'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden')
        return password2






class LoginForm(forms.Form):
    email = forms.CharField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Para cada campo, si tiene error, agrega 'is-invalid' a su clase CSS
        for field_name, field in self.fields.items():
            css_class = field.widget.attrs.get('class', '')
            if self.errors.get(field_name):
                field.widget.attrs['class'] = css_class + ' is-invalid'

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError('Los datos no son correctos')
        return cleaned_data


