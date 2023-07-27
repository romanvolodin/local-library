from datetime import date, timedelta

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from catalog.forms import RenewBookModelForm
from catalog.models import Author, Book, BookInstance, Genre


def index(request):
    book_count = Book.objects.count()
    instance_count = BookInstance.objects.count()
    available_instance_count = BookInstance.objects.filter(status__exact="a").count()
    author_count = Author.objects.count()
    genre_count = Genre.objects.count()
    astronaut_count = Book.objects.filter(title__icontains="Астронавт").count()

    visit_count = request.session.get("visit_count", 0)
    request.session["visit_count"] = visit_count + 1

    context = {
        "book_count": book_count,
        "instance_count": instance_count,
        "available_instance_count": available_instance_count,
        "author_count": author_count,
        "genre_count": genre_count,
        "astronaut_count": astronaut_count,
        "visit_count": visit_count,
    }
    return render(request, "catalog/index.html", context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 20
    template_name = "catalog/book-list.html"


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "catalog/book-detail.html"


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 20
    template_name = "catalog/author-list.html"


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "catalog/author-detail.html"


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    paginate_by = 20
    template_name = "catalog/book-instance-taken-list.html"

    def get_queryset(self):
        return self.request.user.taken_books.all()


class BorrowedBookListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    paginate_by = 20
    template_name = "catalog/book-instance-borrowed-list.html"
    permission_required = ("catalog.can_mark_returned",)

    def get_queryset(self):
        return BookInstance.objects.filter(status="o")


@permission_required("catalog.can_mark_returned")
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == "POST":
        form = RenewBookModelForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data["due_back"]
            book_instance.save()
            return HttpResponseRedirect(reverse("borrowed-books"))
    else:
        proposed_renewal_date = date.today() + timedelta(weeks=3)
        form = RenewBookModelForm(initial={"due_back": proposed_renewal_date})

    context = {
        "form": form,
        "book_instance": book_instance,
    }
    return render(request, "catalog/book-renew.html", context)
