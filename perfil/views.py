from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import copy
from . import models
from . import forms

# Classe base para as views de perfil (criação e atualização)
class BasePerfil(View):
    template_name = 'perfil/criar.html'  # Template padrão para criação de perfil

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)  # Chama o setup da classe pai (View)

        # Cria uma cópia do carrinho da sessão (se existir)
        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))

        self.perfil = None  # Inicializa o perfil como None

        # Verifica se o usuário está autenticado
        if self.request.user.is_authenticated:
            # Obtém o perfil do usuário logado
            self.perfil = models.Perfil.objects.filter(usuario=self.request.user).first()
            # Preenche os formulários com os dados do usuário e perfil
            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user),
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil)
            }
        else:
            # Cria formulários vazios para novos usuários
            self.contexto = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'perfilform': forms.PerfilForm(data=self.request.POST or None)
            }

        # Atribui os formulários ao contexto
        self.userform = self.contexto['userform']
        self.perfilform = self.contexto['perfilform']

        # Altera o template para atualização se o usuário estiver logado
        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'

        # Renderiza o template com o contexto
        self.renderizar = render(self.request, self.template_name, self.contexto)

    # Método GET: exibe o formulário
    def get(self, *args, **kwargs):
        return self.renderizar

# View para criar um novo perfil
class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        # Verifica se os formulários são válidos
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            messages.error(
                self.request,
                'Existem erros no formulário de cadastro. Verifique os campos e preencha corretamente'
            )
            return self.renderizar

        # Obtém os dados validados dos formulários
        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        last_name = self.userform.cleaned_data.get('last_name')
        first_name = self.userform.cleaned_data.get('first_name')

        # Usuário logado (atualização)
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(User, username=self.request.user.username)
            usuario.username = username

            # Atualiza a senha se fornecida
            if password:
                usuario.set_password(password)

            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()  # Salva as alterações no usuário

            # Cria ou atualiza o perfil
            if not self.perfil:
                self.perfilform.cleaned_data['usuario'] = usuario
                perfil = models.Perfil(**self.perfilform.cleaned_data)
                perfil.save()
            else:
                perfil = self.perfilform.save(commit=False)
                perfil.usuario = usuario
                perfil.save()

        # Usuário não logado (criação)
        else:
            # Cria um novo usuário
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            # Cria um novo perfil associado ao usuário
            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        # Autentica o usuário se uma senha foi fornecida
        if password:
            autentica = authenticate(
                self.request,
                username=usuario,
                password=password
            )
            if autentica:
                login(self.request, user=usuario)

        # Restaura o carrinho na sessão
        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()

        # Mensagens de sucesso
        messages.success(
            self.request,
            'Seu cadastro foi criado ou atualizado com sucesso!'
        )
        messages.success(
            self.request,
            'Você fez Login e pode acessar o E-commerce!'
        )

        # Redireciona para o carrinho
        return redirect('produto:carrinho')

# View para atualizar o perfil (não implementada)
class Atualizar(BasePerfil):
    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar')

# View para fazer login
class Login(View):
    def post(self, *args, **kwargs):
        # Obtém o nome de usuário e senha do formulário
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        # Verifica se os campos foram preenchidos
        if not username or not password:
            messages.error(
                self.request,
                'Usuário ou senha inválidos!'
            )
            return redirect('perfil:criar')

        # Autentica o usuário
        usuario = authenticate(self.request, username=username, password=password)

        # Verifica se a autenticação foi bem-sucedida
        if not usuario:
            messages.error(
                self.request,
                'Usuário ou senha inválidos!'
            )
            return redirect('perfil:criar')

        # Faz login e redireciona para o carrinho
        login(self.request, user=usuario)
        messages.success(
            self.request,
            'Você fez Login e pode acessar o E-commerce!'
        )
        return redirect('produto:carrinho')

# View para fazer logout
class Logout(View):
    def get(self, *args, **kwargs):
        # Salva uma cópia do carrinho da sessão
        carrinho = copy.deepcopy(self.request.session.get('carrinho'))

        # Faz logout do usuário
        logout(self.request)

        # Restaura o carrinho na sessão
        self.request.session['carrinho'] = carrinho
        self.request.session.save()

        # Redireciona para a lista de produtos
        return redirect('produto:lista')