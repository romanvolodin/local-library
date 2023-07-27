from django.urls import path

from catalog import views


urlpatterns = [
    path("", views.index, name="index"),
    path("books/", views.BookListView.as_view(), name="books"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
    path("authors/", views.AuthorListView.as_view(), name="authors"),
    path("authors/<int:pk>/", views.AuthorDetailView.as_view(), name="author-detail"),
    path("taken-books/", views.LoanedBooksByUserListView.as_view(), name="taken-books"),
    path("borrowed/", views.BorrowedBookListView.as_view(), name="borrowed-books"),
]
