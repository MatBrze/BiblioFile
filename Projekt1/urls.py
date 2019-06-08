"""Projekt1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from library.views import ReaderView, BookListView, BookDetailsView, AuthorsListView, AuthorDetailsView, MainView, \
    RegisterView, BookListListView, AuthorsListListView, MainSearchView, ContactView, ProfileView, AddToProfileView, \
    DeleteFromProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='index'),
    path('register', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('addtoprofile/<book_id>', AddToProfileView.as_view(), name='add-profile'),
    path('deletefromprofile/<book_id>', DeleteFromProfileView.as_view(), name='delete-profile'),
    path('reader/<book_id>', ReaderView.as_view(), name='reader'),
    path('list/', BookListView.as_view(), name='book-list'),
    path('list_2/', BookListListView.as_view(), name='book-list-li'),
    path('authorlist/', AuthorsListView.as_view(), name='author-list'),
    path('authorlist2/', AuthorsListListView.as_view(), name='author-list-li'),
    path('book/<book_id>', BookDetailsView.as_view(), name='book-details'),
    path('author/<author_id>', AuthorDetailsView.as_view(), name='author-details'),
    path('search', MainSearchView.as_view(), name='main-search'),
    path('contact/', ContactView.as_view(), name='contact')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
