from django.shortcuts import render

from catalog.models import Author, Book, BookInstance, Genre


def index(request):
    book_count = Book.objects.count()
    instance_count = BookInstance.objects.count()
    available_instance_count = BookInstance.objects.filter(status__exact="a").count()
    author_count = Author.objects.count()
    genre_count = Genre.objects.count()
    astronaut_count = Book.objects.filter(title__icontains="Астронавт").count()

    context = {
        "book_count": book_count,
        "instance_count": instance_count,
        "available_instance_count": available_instance_count,
        "author_count": author_count,
        "genre_count": genre_count,
        "astronaut_count": astronaut_count,
    }
    return render(request, "catalog/index.html", context)
