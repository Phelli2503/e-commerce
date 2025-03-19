from django.urls import path  # Importa a função path para definir as URLs
from . import views  # Importa as views do aplicativo atual

# Define o namespace do aplicativo para evitar conflitos de nomes em projetos maiores
app_name = 'produto'

# Lista de URLs do aplicativo 'produto'
urlpatterns = [
    # Rota principal da listagem de produtos (exemplo: /produto/)
    path('', views.ListaProdutos.as_view(), name='lista'),

    # Rota para exibir detalhes de um produto específico usando slug (exemplo: /produto/nome-do-produto/)
    path('<slug>', views.DetalheProduto.as_view(), name='detalhe'),

    # Rota para adicionar um produto ao carrinho (exemplo: /produto/adicionaraocarrinho/)
    path('adicionaraocarrinho/', views.AdicionarAoCarrinho.as_view(), name='adicionaraocarrinho'),

    # Rota para remover um produto do carrinho (exemplo: /produto/removerdocarrinho/)
    path('removerdocarrinho/', views.RemoverDoCarrinho.as_view(), name='removerdocarrinho'),

    # Rota para visualizar o carrinho de compras (exemplo: /produto/carrinho/)
    path('carrinho/', views.Carrinho.as_view(), name='carrinho'),

    # Rota para exibir um resumo da compra antes da finalização (exemplo: /produto/resumodacompra/)
    path('resumodacompra/', views.ResumoDaCompra.as_view(), name='resumodacompra'),

    # Rota para a funcionalidade de busca de produtos (exemplo: /produto/busca/)
    path('busca/', views.Busca.as_view(), name='busca'),
]
