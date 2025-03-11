from django import forms
from django.contrib.auth.models import User
from . import models

class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)

class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha'
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação Senha'
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password2', 'email')

    def clean(self, *args, **kwargs):
        cleaned_data = self.cleaned_data
        validation_error_msgs = {}

        # Dados do formulário
        usuario_data = cleaned_data.get('username')
        password_data = cleaned_data.get('password')
        password2_data = cleaned_data.get('password2')
        email_data = cleaned_data.get('email')

        # Mensagens de erro
        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'As senhas não conferem'
        error_msg_password_short = 'Sua senha precisa ter pelo menos 6 caracteres'

        # Usuário logado: atualização
        if self.usuario:
            usuario_db = User.objects.filter(username=usuario_data).first()
            email_db = User.objects.filter(email=email_data).first()

            if usuario_db and usuario_data != self.usuario.username:
                validation_error_msgs['username'] = error_msg_user_exists

            if email_db and email_data != self.usuario.email:
                validation_error_msgs['email'] = error_msg_email_exists

            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match
                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_short

        # Usuário não logado: cadastro
        else:
            if User.objects.filter(username=usuario_data).exists():
                validation_error_msgs['username'] = error_msg_user_exists

            if User.objects.filter(email=email_data).exists():
                validation_error_msgs['email'] = error_msg_email_exists

            if not password_data:
                validation_error_msgs['password'] = 'Este campo é obrigatório'
            elif len(password_data) < 6:
                validation_error_msgs['password'] = error_msg_password_short
            elif password_data != password2_data:
                validation_error_msgs['password'] = error_msg_password_match
                validation_error_msgs['password2'] = error_msg_password_match

        if validation_error_msgs:
            raise forms.ValidationError(validation_error_msgs)

        return cleaned_data 