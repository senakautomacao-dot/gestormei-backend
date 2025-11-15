from django.db import models

class Receita(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.UUIDField()
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'receitas'
        managed = False

class Compra(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.UUIDField()
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'compras'
        managed = False

class Profile(models.Model):
    id = models.UUIDField(primary_key=True)
    cnpj = models.TextField(null=True)
    razao_social = models.TextField(null=True)
    data_abertura = models.DateField(null=True)

    class Meta:
        db_table = 'profiles'
        managed = False
