from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages


from .models import Book
from .forms import BookForm
from mysite.books.tasks import *




def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})


def save_book_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            req = request.POST["req"]
            status = request.POST["status"]
            descricao = request.POST["descricao"]
            data_agendamento = request.POST["data_agendamento"]
            contato_agendamento = request.POST["contato_agendamento"]
            if status == "":
                data['form_is_valid'] = False
            elif (status == "1" or status == "2"):
                result = set_aceite_recusa(req, descricao, status)
                if (result['tipoarquivo'] == '4' and result['processado'] == '1'):
                    Book.objects.filter(req=req).update(status=status)
                else:
                    data['html_form'] = render_to_string('books/includes/partial_book_delete.html', request=request)
                    return JsonResponse(data) 
            else:
                result = set_atualizacao(req, descricao, status,data_agendamento, contato_agendamento)
                if (result['tipoarquivo'] == '4' and result['processado'] == '1'):
                    Book.objects.filter(req=req).update(status=status)
                else:
                    data['html_form'] = render_to_string('books/includes/partial_book_delete.html', request=request)
                    return JsonResponse(data)
            data['form_is_valid'] = True
            books = Book.objects.all()
            data['html_book_list'] = render_to_string('books/includes/partial_book_list.html', {
                'books': books
            })
        else:
             data['html_form'] = render_to_string('books/includes/partial_book_update.html', request=request)
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST )
    else:
        form = BookForm()
    return save_book_form(request, form,  'books/includes/partial_book_create.html')

def book_database(request):
    data = dict()
    if insert_in_database():
        books = Book.objects.all()
        data['html_book_list'] = render_to_string('books/includes/partial_book_list.html', {
            'books': books
        })
    else:
        data['html_form'] = render_to_string('books/includes/partial_book_update.html', request=request)
    return JsonResponse(data)



def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
    else:
        form = BookForm(instance=book)
    return save_book_form(request, form, 'books/includes/partial_book_update.html')


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk )
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True
        books = Book.objects.all()
        data['html_book_list'] = render_to_string('books/includes/partial_book_list.html', {
            'books': books
        })
    else:
        context = {'book': book}
        data['html_form'] = render_to_string('books/includes/partial_book_delete.html', context, request=request)
    return JsonResponse(data)
