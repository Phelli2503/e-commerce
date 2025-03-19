from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Define as URLs principais do projeto
urlpatterns = [
    # Rota para a aplicação 'produto' (página inicial)
    path('', include('produto.urls')),

    # Rota para a aplicação 'perfil'
    path('perfil/', include('perfil.urls')),

    # Rota para a aplicação 'pedido'
    path('pedido/', include('pedido.urls')),

    # Rota para o painel de administração do Django
    path('admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Adiciona suporte para servir arquivos de mídia durante o desenvolvimento

# TODO: Remover debug toolbar antes de ir para produção
if settings.DEBUG:
    import debug_toolbar
    # Adiciona as URLs da debug toolbar apenas no modo de depuração
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),  # Rota para a debug toolbar
    ] + urlpatterns # é usada para concatenar listas de URLs

        
        # Como o Debug Toolbar Ajuda no Desenvolvimento
        #     Otimização de Desempenho:

        #     Identifica consultas ao banco de dados que podem ser otimizadas.

        #     Ajuda a reduzir o tempo de carregamento das páginas.

        #     Depuração de Erros:

        #     Facilita a identificação de problemas em templates, views, ou consultas ao banco de dados.

        #     Mostra o contexto exato passado para os templates, ajudando a depurar erros de variáveis ausentes ou incorretas.

        #     Entendimento do Fluxo da Aplicação:

        #     Permite entender como o Django processa uma requisição, desde a view até a renderização do template.

        #     Monitoramento de Cache:

        #     Ajuda a verificar se o cache está sendo utilizado corretamente.

        #     Análise de Requisições:

        #     Facilita a visualização de cabeçalhos, cookies, e parâmetros enviados e recebidos.
