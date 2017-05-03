# -*- coding: utf-8 -*-

from django import forms

from .models import Book


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('req' ,'status', 'descricao', 'data_agendamento', 'contato_agendamento' )

