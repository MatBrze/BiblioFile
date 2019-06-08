from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator

from library import models
from library.models import Book, Author, Shelf
from .forms import UserRegisterForm, ContactForm

from random import randint
# Create your views here.


class MainView(View):
    def get(self, request):
        books = models.Book.objects.all()
        random_number = randint(0, len(books)-1)
        random_book = books[random_number]
        authors = models.Author.objects.all()
        random_author_number = randint(0, len(authors)-1)
        random_author = authors[random_author_number]
        short_desc = random_author.biography[:1000] + '...'
        ctx = {
            "random_book": random_book,
            "random_author": random_author,
            'short_desc': short_desc
        }
        return render(request, 'index.html', ctx)


class ReaderView(View):

    def get(self, request, book_id):
        LINES_PER_PAGE = 28
        lines = []
        book = models.Book.objects.get(pk=book_id)
        with open(book.ebook.url) as fileobj:
            for row in fileobj:
                lines.append(row)
        paginator = Paginator(lines, LINES_PER_PAGE)
        page = request.GET.get('page')
        book_page = paginator.get_page(page)
        return render(request, 'reader.html', {'book_page': book_page})


class BookListView(View):

    def get(self, request):
        books = models.Book.objects.all().order_by('title')
        ctx = {'books': books}
        return render(request, 'all_books_list.html', ctx)


class BookListListView(View):

    def get(self, request):
        books = models.Book.objects.all().order_by('title')
        ctx = {'books': books}
        return render(request, 'all_books_list_li.html', ctx)


class BookDetailsView(LoginRequiredMixin, View):

    def get(self, request, book_id):
        book = models.Book.objects.get(pk=book_id)
        current_user = request.user
        shelf_book = Shelf.objects.filter(user=current_user).filter(book=book)
        ctx = {
            'book': book,
            'shelf_book': shelf_book
               }
        return render(request, 'book_details.html', ctx)


class AuthorsListView(View):

    def get(self, request):
        authors = models.Author.objects.all().order_by('surname')
        ctx = {'authors': authors}
        return render(request, 'all_authors_list.html', ctx)


class AuthorsListListView(View):

    def get(self, request):
        authors = models.Author.objects.all().order_by('surname')
        ctx = {'authors': authors}
        return render(request, 'all_authors_list_li.html', ctx)


class AuthorDetailsView(LoginRequiredMixin, View):

    def get(self, request, author_id):
        author = models.Author.objects.get(pk=author_id)
        books = models.Book.objects.filter(authors=author_id)
        ctx = {'author': author,
               'books': books}
        return render(request, 'author_details.html', ctx)


class MainSearchView(View):

    def get(self, request):
        return render(request, "main_search.html")

    def post(self, request):
        title = request.POST.get('title')
        books = Book.objects.filter(title__icontains=title)
        authors = Author.objects.filter(surname__icontains=title)
        names = Author.objects.filter(name__icontains=title)
        ctx = {
            'books': books,
            'authors': authors,
            'names': names
        }
        return render(request, "main_search.html", ctx)


class RegisterView(View):

    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'{user} Konto zostało utworzone! Zaloguj się')
            return redirect('login')
        return render(request, 'register.html', {'form': form})


class ContactView(View):

    def get(self, request):
        form = ContactForm()
        return render(request, 'contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Wiadomość przesłana')
            return redirect('contact')
        return render(request, 'contact.html', {'form': form})


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        current_user = request.user
        books = Shelf.objects.filter(user=current_user).distinct()
        ctx = {'books': books}
        return render(request, 'profile.html', ctx)


class AddToProfileView(View):

    def get(self, request, book_id):
        current_user = request.user
        book = models.Book.objects.get(pk=book_id)
        shelf_book = Shelf.objects.filter(user=current_user).filter(book=book)
        new_shelf = Shelf(user=current_user, book=book)
        new_shelf.save()
        ctx = {
            'book': book,
            'shelf_book': shelf_book
        }
        return render(request, 'book_details.html', ctx)


class DeleteFromProfileView(View):

    def get(self, request, book_id):
        book = models.Book.objects.get(pk=book_id)
        current_user = request.user
        shelf_book = Shelf.objects.filter(user=current_user).filter(book=book)
        instance = models.Shelf.objects.get(book=book)
        instance.delete()
        ctx = {
            'shelf_book': shelf_book,
            'book': book
        }
        return render(request, 'book_details.html', ctx)
