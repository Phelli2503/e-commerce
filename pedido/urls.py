from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    # Pega o pk do pagamento para enviar para a página de pagamento
    path('pagar/<int:pk>', views.Pagar.as_view(), name='pagar'),
    path('salvarpedido/', views.SalvarPedido.as_view(), name='salvarpedido'),
    path('lista/', views.Lista.as_view(), name='lista'),
    # Detalhes do pedido, através do pk do pedido
    path('detalhe/<int:pk>', views.Detalhe.as_view(), name='detalhe'),

]
