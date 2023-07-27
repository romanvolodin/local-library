from django.contrib import admin

from catalog.models import Author, Book, BookInstance, Genre, Language


class BookInline(admin.TabularInline):
    model = Book
    extra = 0
    fields = ("title", "isbn", "language")


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "last_name",
        "first_name",
        "date_of_birth",
        "date_of_death",
    )
    fields = (
        "first_name",
        "last_name",
        ("date_of_birth", "date_of_death"),
    )
    inlines = (BookInline,)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "display_genre",
    )
    inlines = (BookInstanceInline,)

    def display_genre(self, book):
        return ", ".join([genre.name for genre in book.genre.all()[:3]])

    display_genre.short_description = "Жанр"


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "status",
        "borrower",
        "due_back",
        "id",
    )
    list_filter = (
        "status",
        "due_back",
    )
    fieldsets = (
        (None, {"fields": ("book", "imprint", "id")}),
        (" Доступность", {"fields": ("status", "borrower", "due_back")}),
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass
