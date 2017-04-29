from __future__ import unicode_literals

from django.db import models


class Book(models.Model):
    Aceito = 1 
    Recuso = 2 
    Pendente = 3 
    Atualizacao = 1 
    Cancelado = 4 
    Resolvido = 5 
    Agendamento = 2 
    
    STATUS = (
        (Aceito , 'Aceito'),
        (Recuso , 'Recuso'),
        (Pendente , 'Pendente'),
        (Atualizacao , 'Atualizacao'),
        (Cancelado , 'Cancelado'),
        (Resolvido , 'Resolvido'),
        (Agendamento , 'Agendamento'),
    )
    idarquivo = models.CharField(max_length=512)
    req = models.CharField(max_length=512)
    wo = models.CharField(max_length=512)
    datahorageracaoarquivo = models.CharField(max_length=512)
    data_agendamento = models.CharField(max_length=512, blank=True, null=True)
    descricao =  models.TextField()
    status = models.PositiveSmallIntegerField(choices=STATUS, blank=True, null=True)
    contato_agendamento = models.CharField(max_length=512, blank=True, null=True)


# class Integracao(models.Model):
#     idarquivo = models.CharField(max_length=512)
#     req = models.CharField(max_length=512)
#     wo = models.CharField(max_length=512)
#     datahorageracaoarquivo = models.CharField(max_length=512)

#     def __str__(self):
#         return self.idarquivo