from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from produto.models import Variacao

from utils import utils
from .models import Pedido, ItemPedido

# Mixin para verificar se o usuário está autenticado antes de acessar uma view
class DispatchRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        # Verifica se o usuário está autenticado
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')  # Redireciona para a página de criação de perfil
        return super().dispatch(self.request, *args, **kwargs)
    
    # Filtra os pedidos para mostrar apenas os do usuário logado
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(usuario=self.request.user)  # Filtra os pedidos pelo usuário atual
        return qs

# View para a página de pagamento de um pedido
class Pagar(DispatchRequiredMixin, DetailView):
    template_name = 'pedido/pagar.html'  # Template usado para renderizar a página
    model = Pedido  # Modelo associado à view
    pk_url_kwarg = 'pk'  # Nome do parâmetro da URL que contém o ID do pedido
    context_object_name = 'pedido'  # Nome do objeto no contexto do template

# View para salvar um pedido
class SalvarPedido(View):
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        # Verifica se o usuário está autenticado
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa fazer login.'
            )
            return redirect('perfil:criar')  # Redireciona para a página de criação de perfil

        # Verifica se o carrinho está vazio
        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Carrinho Vazio.'
            )
            return redirect('produtos:lista')  # Redireciona para a lista de produtos

        # Obtém o carrinho da sessão
        carrinho = self.request.session.get('carrinho')
        # Obtém os IDs das variações no carrinho
        carrinho_variacao_ids = [v for v in carrinho]
        # Busca as variações no banco de dados
        bd_variacoes = list(Variacao.objects.select_related('produto')
                            .filter(id__in=carrinho_variacao_ids))

        # Verifica o estoque para cada variação no carrinho
        for variacao in bd_variacoes:
            vid = str(variacao.id)

            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_unitario_promocional']

            error_msg_estoque = ''

            # Verifica se o estoque é suficiente
            if estoque < qtd_carrinho:
                # Ajusta a quantidade no carrinho para o estoque disponível
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unt
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * preco_unt_promo

                error_msg_estoque = 'Estoque insuficiente para alguns produtos do seu carrinho '\
                                   'Reduzimos a quantidade desses produtos. Por favor, verifique '\
                                   'quais produtos foram afetados a seguir.'

                messages.error(
                    self.request,
                    error_msg_estoque
                )

                self.request.session.save()  # Salva a sessão com as alterações
                return redirect('produto:carrinho')  # Redireciona para o carrinho

        # Calcula a quantidade total e o valor total do carrinho
        qtd_total_carrinho = utils.cart_total_qtd(carrinho)
        valor_total_carrinho = utils.cart_totals(carrinho)

        # Cria um novo pedido
        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status='C',  # Status 'Criado'
        )
        
        pedido.save()

        # Cria os itens do pedido em lote (bulk_create)
        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=v['produto_nome'],
                    produto_id=v['produto_id'],
                    variacao=v['variacao_nome'],
                    variacao_id=v['variacao_id'],
                    preco=v['preco_quantitativo'],
                    preco_promocional=v['preco_quantitativo_promocional'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem'],
                ) for v in carrinho.values()
            ]
        )

        # Remove o carrinho da sessão após finalizar o pedido
        del self.request.session['carrinho']
        # Redireciona para a página de pagamento do pedido
        return redirect(
            reverse(
                'pedido:pagar',
                kwargs={
                    'pk': pedido.pk
                }
            )
        )

# View para exibir os detalhes de um pedido
class Detalhe(DispatchRequiredMixin, DetailView):
    model = Pedido  # Modelo associado à view
    context_object_name = 'pedido'  # Nome do objeto no contexto do template
    tamplate_name = 'pedido/detalhe.html'  # Template usado para renderizar a página
    pk_url_kwarg = 'pk'  # Nome do parâmetro da URL que contém o ID do pedido

# View para listar os pedidos do usuário
class Lista(DispatchRequiredMixin, ListView):
    model = Pedido  # Modelo associado à view
    context_object_name = 'pedidos'  # Nome da lista de objetos no contexto do template
    tamplate_name = 'pedido/lista.html'  # Template usado para renderizar a página
    paginate_by = 10  # Número de itens por página
    ordering = ['-id']  # Ordena os pedidos por ID decrescente