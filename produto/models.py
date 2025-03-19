from django.db import models
from PIL import Image
import os
from django.conf import settings
from django.utils.text import slugify

# Modelo para armazenar informações sobre um produto
class Produto(models.Model):
    # Nome do produto
    nome = models.CharField(max_length=250)

    # Descrição curta do produto (máx. 250 caracteres)
    descricao_curta = models.TextField(max_length=250)

    # Descrição longa do produto (máx. 250 caracteres)
    descricao_longa = models.TextField(max_length=250)

    # Imagem do produto, armazenada em 'produto_imagens/ano/mês/'
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m', blank=True, null=True)

    # Slug gerado automaticamente a partir do nome para URLs amigáveis
    slug = models.SlugField(unique=True, blank=True, null=True)

    # Preço normal do produto
    preco_marketing = models.FloatField(verbose_name='Preço')

    # Preço promocional (padrão: 0)
    preco_marketing_promocional = models.FloatField(default=0, verbose_name='Preço Promo.')

    # Tipo do produto: 'V' para variável (exemplo: diferentes tamanhos/cores), 'S' para simples
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples'),
        )
    )

    # Método para formatar o preço no padrão brasileiro (R$ X,XX)
    def get_preco_formatado(self):
        return f'R$ {self.preco_marketing:.2f}'.replace('.', ',')
    get_preco_formatado.short_description = 'Preço'

    # Método para formatar o preço promocional no padrão brasileiro
    def get_preco_promocional_formatado(self):
        return f'R$ {self.preco_marketing_promocional:.2f}'.replace('.', ',')
    get_preco_promocional_formatado.short_description = 'Preço Promo.'

    # Método estático para redimensionar imagens para um tamanho máximo de 800px de largura
    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)  # Caminho completo da imagem
        img_pil = Image.open(img_full_path)  # Abre a imagem usando Pillow
        original_width, original_height = img_pil.size  # Obtém as dimensões originais da imagem

        # Se a largura já for menor que o limite, não faz nada
        if original_width <= new_width:
            img_pil.close()
            return

        # Calcula a nova altura proporcional à nova largura
        new_height = round((new_width * original_height) / original_width)

        # Redimensiona a imagem mantendo a qualidade
        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)

        # Salva a nova imagem otimizada com qualidade reduzida para economizar espaço
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50,
        )

    # Sobrescreve o método save() para gerar automaticamente o slug e redimensionar a imagem
    def save(self, *args, **kwargs):
        # Se o slug não estiver definido, cria um a partir do nome do produto
        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug 

        # Salva o objeto normalmente
        super().save(*args, **kwargs)

        # Define o tamanho máximo para a imagem
        max_image_size = 800

        # Se houver uma imagem associada ao produto, redimensiona
        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    # Representação em string do objeto (aparece no admin do Django)
    def __str__(self):
        return self.nome
    

# Modelo para variações de um produto (exemplo: tamanhos, cores)
class Variacao(models.Model):
    # Relacionamento com um produto específico (se um produto for deletado, suas variações também são)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    # Nome da variação (opcional, pois pode ser gerado automaticamente pelo nome do produto)
    nome = models.CharField(max_length=50, blank=True, null=True)

    # Preço da variação
    preco = models.FloatField()

    # Preço promocional da variação (padrão: 0)
    preco_promocional = models.FloatField(default=0)

    # Quantidade em estoque da variação
    estoque = models.PositiveIntegerField(default=1)

    # Retorna o nome da variação ou, se não houver, o nome do produto
    def __str__(self):
        return self.nome or self.produto.nome

    # Configuração para exibição no painel administrativo do Django
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
