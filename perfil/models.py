from django.db import models

# os models fazem referencia ao banco de dados
# o django possui arm proprio (substitui a linguagem sql por classes e queries python)
# tabelas são classes python

# herda de models.Model para o django sabe que essa classe é referente 
# a uma tabela do banco de dados.
# os atributos da classe são as colunas do banco

class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0.0)

    def __str__(self):
        return self.categoria

class Conta(models.Model):
    banco_choices = (
        ('NU', 'Nubank'),
        ('CE', 'Caixa Economica')
    )

    tipo_choices = (
        ('PF', 'Pessoa Fisica'),
        ('PJ', 'Pessoa Juridica')
    )
    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length=2, choices=banco_choices)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    valor = models.FloatField()
    icone = models.ImageField(upload_to='icones')

    def __str__(self):
        return self.apelido