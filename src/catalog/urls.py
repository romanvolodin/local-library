from django.urls import path

from catalog import views


urlpatterns = [
    path("", views.index, name="index"),
    path("books/", views.BookListView.as_view(), name="books"),
    path("books/create/", views.BookCreate.as_view(), name="book-create"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
    path("books/<int:pk>/update/", views.BookUpdate.as_view(), name="book-update"),
    path("books/<int:pk>/delete/", views.BookDelete.as_view(), name="book-delete"),
    path("authors/", views.AuthorListView.as_view(), name="authors"),
    path("authors/create/", views.AuthorCreate.as_view(), name="author-create"),
    path("authors/<int:pk>/", views.AuthorDetailView.as_view(), name="author-detail"),
    path("authors/<int:pk>/update/", views.AuthorUpdate.as_view(), name="author-update"),
    path("authors/<int:pk>/delete/", views.AuthorDelete.as_view(), name="author-delete"),
    path("taken-books/", views.LoanedBooksByUserListView.as_view(), name="taken-books"),
    path("borrowed/", views.BorrowedBookListView.as_view(), name="borrowed-books"),
    path("book/<str:pk>/renew/", views.renew_book_librarian, name="renew-book-librarian"),
]
