from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=30)
    owner = models.CharField(max_length=30)
    saldo = models.CharField(max_length=10, null=True)


class Transaction(models.Model):
    tipo = models.CharField(max_length=25)
    data = models.DateTimeField()
    valor = models.CharField(max_length=10)
    cpf = models.CharField(max_length=11)
    cartao = models.CharField(max_length=12)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="transactions")