from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from . import models
from perfil.models import Perfil

# View para listar todos os produtos
class ListaProdutos(ListView):
    model = models.Produto  # Modelo associado à view
    template_name = 'produto/lista.html'  # Template usado para renderizar a lista de produtos
    context_object_name = 'produtos'  # Nome do objeto no contexto do template
    paginate_by = 5  # Número de itens por página
    ordering = ['-id']  # Ordena os produtos por ID decrescente

# View para realizar buscas de produtos
class Busca(ListaProdutos):
    def get_queryset(self, *args, **kwargs):
        # Obtém o termo de busca da URL ou da sessão
        termo = self.request.GET.get('termo') or self.request.session['termo']
        qs = super().get_queryset(*args, **kwargs)  # Obtém o queryset da classe pai (ListaProdutos)

        # Se não houver termo de busca, retorna o queryset original
        if not termo:
            return qs

        # Salva o termo de busca na sessão
        self.request.session['termo'] = termo

        # Filtra os produtos com base no termo de busca
        qs = qs.filter(
            Q(nome__icontains=termo) |  # Busca no nome do produto
            Q(descricao_curta__icontains=termo) |  # Busca na descrição curta
            Q(descricao_longa__icontains=termo)  # Busca na descrição longa
        )

        self.request.session.save()  # Salva a sessão
        return qs

# View para exibir os detalhes de um produto específico
class DetalheProduto(DetailView):
    model = models.Produto  # Modelo associado à view
    template_name = 'produto/detalhe.html'  # Template usado para renderizar os detalhes do produto
    context_object_name = 'produto'  # Nome do objeto no contexto do template
    slug_url_kwarg = 'slug'  # Nome do parâmetro da URL que contém o slug do produto

# View para adicionar um produto ao carrinho
class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        # Obtém a URL de referência (de onde o usuário veio)
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')  # Redireciona para a lista de produtos se não houver referência
        )
        variacao_id = self.request.GET.get('vid')  # Obtém o ID da variação do produto

        # Verifica se o ID da variação foi fornecido
        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            return redirect(http_referer)

        # Obtém a variação do produto ou retorna um erro 404 se não existir
        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque  # Estoque da variação
        produto = variacao.produto  # Produto associado à variação
        produto_id = produto.id  # ID do produto
        produto_nome = produto.nome  # Nome do produto
        variacao_nome = variacao.nome or ''  # Nome da variação (se existir)
        preco_unitario = variacao.preco  # Preço unitário da variação
        preco_unitario_promocional = variacao.preco_promocional  # Preço promocional da variação
        quantidade = 1  # Quantidade inicial
        slug = produto.slug  # Slug do produto
        imagem = produto.imagem  # Imagem do produto

        # Verifica se a imagem existe
        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        # Verifica se há estoque suficiente
        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'
            )
            return redirect(http_referer)

        # Inicializa o carrinho na sessão se não existir
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']  # Obtém o carrinho da sessão

        # Verifica se a variação já está no carrinho
        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1  # Incrementa a quantidade

            # Verifica se o estoque é suficiente para a quantidade desejada
            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no '
                    f'produto {produto_nome}. Adicionamos {variacao_estoque}x '
                    f'no seu carrinho.'
                )
                quantidade_carrinho = variacao_estoque

            # Atualiza a quantidade e os preços no carrinho
            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho

        else:
            # Adiciona a variação ao carrinho
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional': preco_unitario_promocional,
                'quantidade': 1,
                'slug': slug,
                'imagem': imagem,
            }

        self.request.session.save()  # Salva a sessão

        # Mensagem de sucesso
        messages.success(
            self.request,
            f'Produto {produto.nome} {variacao_nome} adicionado ao seu '
            f'carrinho {carrinho[variacao_id]["quantidade"]}x.'
        )
        return redirect(http_referer)

# View para remover um produto do carrinho
class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        # Obtém a URL de referência (de onde o usuário veio)
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')  # Redireciona para a lista de produtos se não houver referência
        )
        variacao_id = self.request.GET.get('vid')  # Obtém o ID da variação do produto

        # Verifica se o ID da variação foi fornecido
        if not variacao_id:
            return redirect(http_referer)

        # Verifica se o carrinho existe e se a variação está no carrinho
        if 'carrinho' not in self.request.session or variacao_id not in self.request.session['carrinho']:
            return redirect(http_referer)

        # Remove a variação do carrinho
        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()  # Salva a sessão

        # Mensagem de sucesso
        messages.success(
            self.request,
            'Item removido do carrinho com sucesso!'
        )

        return redirect(http_referer)

# View para exibir o carrinho de compras
class Carrinho(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho', {})  # Obtém o carrinho da sessão
        }
        return render(self.request, 'produto/carrinho.html', contexto)  # Renderiza o template do carrinho

# View para exibir o resumo da compra
class ResumoDaCompra(View):
    def get(self, *args, **kwargs):
        # Verifica se o usuário está autenticado
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        # Verifica se o usuário tem um perfil
        perfil = Perfil.objects.filter(usuario=self.request.user).exists()
        if not perfil:
            messages.error(
                self.request,
                'Usuario sem perfil.'
            )
            return redirect('perfil:criar')

        # Verifica se o carrinho está vazio
        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Carrinho vazio.'
            )
            return redirect('produto:lista')

        # Contexto para o template
        contexto = {
            'usuario': self.request.user,  # Usuário logado
            'carrinho': self.request.session['carrinho'],  # Carrinho da sessão
        }
        return render(self.request, 'produto/resumodacompra.html', contexto)  # Renderiza o template do resumo da compra