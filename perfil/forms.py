from django import forms
from django.contrib.auth.models import User
from . import models

# Formulário para o modelo Perfil
class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil  # Modelo associado ao formulário
        fields = '__all__'  # Inclui todos os campos do modelo
        exclude = ('usuario',)  # Exclui o campo 'usuario' do formulário

# Formulário para o modelo User (usuário)
class UserForm(forms.ModelForm):
    # Campo de senha (opcional, pois pode ser uma atualização)
    password = forms.CharField(
        required=False,  # Não é obrigatório (útil para atualizações)
        widget=forms.PasswordInput(),  # Renderiza como um campo de senha
        label='Senha'  # Rótulo do campo
    )

    # Campo de confirmação de senha (opcional)
    password2 = forms.CharField(
        required=False,  # Não é obrigatório
        widget=forms.PasswordInput(),  # Renderiza como um campo de senha
        label='Confirmação Senha'  # Rótulo do campo
    )

    # Método __init__ para personalizar o formulário
    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Chama o __init__ da classe pai (ModelForm)
        self.usuario = usuario  # Armazena o usuário atual (útil para atualizações)

    class Meta:
        model = User  # Modelo associado ao formulário
        fields = ('first_name', 'last_name', 'username', 'password', 'password2', 'email')  # Campos incluídos no formulário

    # Método para validar os dados do formulário
    def clean(self, *args, **kwargs):
        cleaned_data = self.cleaned_data  # Dados validados do formulário
        validation_error_msgs = {}  # Dicionário para armazenar mensagens de erro

        # Obtém os dados do formulário
        usuario_data = cleaned_data.get('username')  # Nome de usuário
        password_data = cleaned_data.get('password')  # Senha
        password2_data = cleaned_data.get('password2')  # Confirmação de senha
        email_data = cleaned_data.get('email')  # E-mail

        # Mensagens de erro pré-definidas
        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'As senhas não conferem'
        error_msg_password_short = 'Sua senha precisa ter pelo menos 6 caracteres'

        # Validações para usuário logado (atualização)
        if self.usuario:
            usuario_db = User.objects.filter(username=usuario_data).first()  # Busca usuário no banco
            email_db = User.objects.filter(email=email_data).first()  # Busca e-mail no banco

            # Verifica se o nome de usuário já existe (exceto para o usuário atual)
            if usuario_db and usuario_data != self.usuario.username:
                validation_error_msgs['username'] = error_msg_user_exists

            # Verifica se o e-mail já existe (exceto para o e-mail atual)
            if email_db and email_data != self.usuario.email:
                validation_error_msgs['email'] = error_msg_email_exists

            # Validações de senha (se fornecida)
            if password_data:
                if password_data != password2_data:  # Verifica se as senhas coincidem
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match
                if len(password_data) < 6:  # Verifica o comprimento da senha
                    validation_error_msgs['password'] = error_msg_password_short

        # Validações para usuário não logado (cadastro)
        else:
            # Verifica se o nome de usuário já existe
            if User.objects.filter(username=usuario_data).exists():
                validation_error_msgs['username'] = error_msg_user_exists

            # Verifica se o e-mail já existe
            if User.objects.filter(email=email_data).exists():
                validation_error_msgs['email'] = error_msg_email_exists

            # Validações de senha
            if not password_data:  # Verifica se a senha foi fornecida
                validation_error_msgs['password'] = 'Este campo é obrigatório'
            elif len(password_data) < 6:  # Verifica o comprimento da senha
                validation_error_msgs['password'] = error_msg_password_short
            elif password_data != password2_data:  # Verifica se as senhas coincidem
                validation_error_msgs['password'] = error_msg_password_match
                validation_error_msgs['password2'] = error_msg_password_match

        # Se houver erros, levanta uma exceção de validação
        if validation_error_msgs:
            raise forms.ValidationError(validation_error_msgs)

        # Retorna os dados validados
        return cleaned_data