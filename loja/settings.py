import os
from pathlib import Path
from django.contrib.messages import constants

# Define o diretório base do projeto (dois níveis acima do arquivo atual)
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações de segurança
SECRET_KEY = 'django-insecure-ej%d^d=u5p@ss=-*7#x*nv&@lfhwb380kx_g3u)@rg-4kg=gsa'  # Chave secreta para criptografia (NUNCA compartilhe em produção)
DEBUG = True  # Ativa o modo de depuração (desative em produção)
ALLOWED_HOSTS = []  # Lista de hosts permitidos (vazia significa apenas localhost)

# Aplicações instaladas no projeto
INSTALLED_APPS = [
    # Apps padrão do Django
    'django.contrib.admin',  # Interface de administração
    'django.contrib.auth',  # Sistema de autenticação
    'django.contrib.contenttypes',  # Gerenciamento de tipos de conteúdo
    'django.contrib.sessions',  # Gerenciamento de sessões
    'django.contrib.messages',  # Sistema de mensagens
    'django.contrib.staticfiles',  # Gerenciamento de arquivos estáticos

    # Apps personalizados
    'produto',  # App para gerenciamento de produtos
    'pedido',  # App para gerenciamento de pedidos
    'perfil',  # App para gerenciamento de perfis de usuários

    # Bibliotecas de terceiros
    'crispy_forms',  # Melhora a renderização de formulários
    'crispy_bootstrap4',  # Template pack do Bootstrap 4 para crispy_forms

    # TODO: Remover debug toolbar antes de ir para produção
    'debug_toolbar',  # Ferramenta de depuração para desenvolvedores
]

# Configuração do crispy_forms para usar o Bootstrap 4
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Middlewares (processadores de requisições/respostas)
MIDDLEWARE = [
    # Middlewares padrão do Django
    'django.middleware.security.SecurityMiddleware',  # Segurança básica
    'django.contrib.sessions.middleware.SessionMiddleware',  # Gerenciamento de sessões
    'django.middleware.common.CommonMiddleware',  # Processamento de requisições comuns
    'django.middleware.csrf.CsrfViewMiddleware',  # Proteção contra CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Autenticação de usuários
    'django.contrib.messages.middleware.MessageMiddleware',  # Sistema de mensagens
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Proteção contra clickjacking

    # TODO: Remover debug toolbar antes de ir para produção
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # Middleware da debug toolbar
]

# Configuração das URLs principais do projeto
ROOT_URLCONF = 'loja.urls'

# Configuração de templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Usa o sistema de templates do Django
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Define o diretório global de templates
        'APP_DIRS': True,  # Permite que o Django procure templates dentro de cada app
        'OPTIONS': {
            'context_processors': [
                # Processadores de contexto padrão
                'django.template.context_processors.debug',  # Adiciona variáveis de depuração
                'django.template.context_processors.request',  # Adiciona o objeto 'request'
                'django.contrib.auth.context_processors.auth',  # Adiciona o usuário autenticado
                'django.contrib.messages.context_processors.messages',  # Adiciona mensagens
            ],
        },
    },
]

# Configuração do WSGI para deploy
WSGI_APPLICATION = 'loja.wsgi.application'

# Configuração do banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Usa SQLite como banco de dados
        'NAME': BASE_DIR / 'db.sqlite3',  # Caminho para o arquivo do banco de dados
    }
}

# Validações de senha
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Verifica similaridade com atributos do usuário
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Exige um comprimento mínimo de senha
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Bloqueia senhas comuns
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Bloqueia senhas totalmente numéricas
    },
]

# Configurações de internacionalização
LANGUAGE_CODE = 'pt-br'  # Idioma padrão: português do Brasil
TIME_ZONE = 'America/Bahia'  # Fuso horário: Bahia
USE_I18N = True  # Ativa a internacionalização
USE_TZ = True  # Usa fuso horário

# Configurações de arquivos estáticos e de mídia
STATIC_URL = '/static/'  # URL base para arquivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # Diretório onde os arquivos estáticos serão coletados para produção
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'templates/static')]  # Diretórios adicionais para arquivos estáticos

MEDIA_URL = '/media/'  # URL base para arquivos de mídia
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Diretório para upload de arquivos de mídia

# Tags para mensagens de alerta
MESSAGE_TAGS = {
    constants.DEBUG: 'alert-info',  # Mensagens de depuração
    constants.ERROR: 'alert-danger',  # Mensagens de erro
    constants.INFO: 'alert-info',  # Mensagens informativas
    constants.SUCCESS: 'alert-success',  # Mensagens de sucesso
    constants.WARNING: 'alert-warning',  # Mensagens de aviso
}

# Configurações de sessão
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # Duração da sessão: 7 dias (em segundos)
SESSION_SAVE_EVERY_REQUEST = False  # Não salva a sessão a cada requisição

# Configuração da debug toolbar (apenas para desenvolvimento)
INTERNAL_IPS = ['127.0.0.1']  # IPs que podem acessar a debug toolbar

# Configuração do campo primário padrão para modelos
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Usa BigAutoField como campo primário padrão