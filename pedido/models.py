from django.db import models
from django.contrib.auth.models import User

# Modelo que representa um pedido feito por um usuário
class Pedido(models.Model):
    # Relacionamento com o modelo User (um usuário pode ter vários pedidos)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    # Campo para armazenar o valor total do pedido
    total = models.FloatField()

    # Campo para armazenar a quantidade total de itens no pedido
    qtd_total = models.PositiveIntegerField()

    # Campo para armazenar o status do pedido
    status = models.CharField(
        default='C',  # Valor padrão: 'Criado'
        max_length=1,  # Tamanho máximo do campo
        choices=(  # Opções de status disponíveis
            ('A', 'Aprovado'),  # Pedido aprovado
            ('C', 'Criado'),  # Pedido criado
            ('R', 'Reprovado'),  # Pedido reprovado
            ('P', 'Pendente'),  # Pedido pendente
            ('E', 'Enviado'),  # Pedido enviado
            ('F', 'Finalizado'),  # Pedido finalizado
        )
    )

    # Método para representar o pedido como uma string (usado no admin e em outros lugares)
    def __str__(self):
        return f'Pedido N. {self.pk}'  # Retorna o número do pedido (primary key)


# Modelo que representa um item de um pedido
class ItemPedido(models.Model):
    # Relacionamento com o modelo Pedido (um pedido pode ter vários itens)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)

    produto = models.CharField(max_length=255)

    # ID do produto no banco de dados (para referência)
    produto_id = models.PositiveIntegerField()

    # Nome da variação do produto (tamanho, cor, etc.)
    variacao = models.CharField(max_length=255)

    # ID da variação do produto no banco de dados (para referência)
    variacao_id = models.PositiveIntegerField()

    # Preço do produto no momento da compra
    preco = models.FloatField()

    # Preço promocional do produto (opcional, padrão é 0)
    preco_promocional = models.FloatField(default=0)

    # Quantidade do produto no pedido
    quantidade = models.PositiveIntegerField()

    # URL ou caminho da imagem do produto
    imagem = models.CharField(max_length=2000)

    # Método para representar o item do pedido como uma string
    def __str__(self):
        return f'Item do {self.pedido}'  # Retorna uma referência ao pedido associado

    # Classe Meta para configurações adicionais do modelo
    class Meta:
        verbose_name = 'Item do pedido'  # Nome singular do modelo (usado no admin)
        verbose_name_plural = 'Itens do pedido'  # Nome plural do modelo (usado no admin)