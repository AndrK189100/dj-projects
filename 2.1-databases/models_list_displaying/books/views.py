from django.http import Http404
from django.shortcuts import render
from books.models import Book
from django.core.paginator import Paginator


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {'books': books}
    return render(request, template, context)


def books_view_pub_date(request, pub_date):
    template = 'books/books_list.html'
    try:
        book = Book.objects.get(pub_date=pub_date)
        books = [book]
    except Book.DoesNotExist:
        raise Http404

    try:
        previous_book = book.get_previous_by_pub_date()
    except:
        previous_book = None

    try:
        next_book = book.get_next_by_pub_date()
    except:
        next_book = None

    context = {'books': books, 'previous_book': previous_book, 'next_book': next_book}
    return render(request, template, context)
