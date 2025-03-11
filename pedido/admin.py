from django.contrib import admin
from .models import Pedido, ItemPedido  # Importação direta dos modelos

# Registrar ItemPedido como um inline dentro de Pedido
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1  # Define quantos campos vazios adicionais serão exibidos no formulário do admin

# Configuração do admin para Pedido
class PedidoAdmin(admin.ModelAdmin):
    inlines = [ItemPedidoInline]  # Adiciona o inline de ItemPedido dentro de Pedido no admin

# Registrar os modelos no Django Admin
admin.site.register(Pedido, PedidoAdmin)  # Registrar Pedido com a customização
admin.site.register(ItemPedido)  # Registrar ItemPedido separadamente
