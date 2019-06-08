from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    biography = models.TextField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True, upload_to="images/")

    def __str__(self):
        return '{} {}'.format(self.name, self.surname)


class Book(models.Model):
    title = models.CharField(max_length=64)
    authors = models.ManyToManyField(Author)
    description = models.TextField(blank=True, null=True)
    cover = models.ImageField(blank=True, null=True, upload_to="images/")
    ebook = models.FileField(blank=True, null=True, upload_to="books/")

    def __str__(self):
        return '{} - {}'.format(self.title, self.authors.get())


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Shelf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.book.title, self.book.authors.get())
