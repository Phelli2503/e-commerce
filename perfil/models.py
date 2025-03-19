from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
import re
from utils.validacpf import valida_cpf  # Importa a função de validação de CPF

# Modelo que representa o perfil de um usuário
class Perfil(models.Model):
    # Relacionamento um-para-um com o modelo User (cada usuário tem um perfil)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")

    # Campo para armazenar a idade do usuário
    idade = models.PositiveIntegerField()

    # Campo para armazenar a data de nascimento do usuário
    data_nascimento = models.DateField()

    # Campo para armazenar o CPF do usuário
    cpf = models.CharField(max_length=11)

    # Campos para armazenar o endereço do usuário
    endereco = models.CharField(max_length=50)  # Nome da rua/avenida
    numero = models.CharField(max_length=5)  # Número da residência
    complemento = models.CharField(max_length=30)  # Complemento (opcional)
    bairro = models.CharField(max_length=30)  # Bairro
    cep = models.CharField(max_length=8)  # CEP (apenas números)
    cidade = models.CharField(max_length=30)  # Cidade
    estado = models.CharField(
        max_length=2,  # Sigla do estado (2 caracteres)
        default='BA',  # Valor padrão: Bahia
        choices=(  # Opções de estados brasileiros
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    # Método para representar o perfil como uma string
    def __str__(self):
        return f'{self.usuario.first_name} {self.usuario.last_name}'  # Retorna o nome completo do usuário

    # Método para validação personalizada dos campos
    def clean(self):
        error_messages = {}  # Dicionário para armazenar mensagens de erro

        # Valida o CPF usando a função valida_cpf
        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido'

        # Valida o CEP (deve conter apenas números e ter 8 dígitos)
        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            error_messages['cep'] = 'CEP inválido, digite os 8 dígitos do CEP'

        # Se houver erros, levanta uma exceção de validação
        if error_messages:
            raise ValidationError(error_messages)

    # Classe Meta para configurações adicionais do modelo
    class Meta:
        verbose_name = 'Perfil'  # Nome singular do modelo (usado no admin)
        verbose_name_plural = 'Perfis'  # Nome plural do modelo (usado no admin)