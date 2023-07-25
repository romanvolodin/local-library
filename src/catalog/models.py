import uuid

from django.db import models
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(
        "жанр",
        max_length=120,
        help_text="Введите жанр книги (например Фантастика, Поэзия и т.д.)",
    )

    def __str__(self) -> str:
        return f"{self.name}"


class Book(models.Model):
    title = models.CharField(
        "название",
        max_length=200,
    )
    author = models.ForeignKey(
        "Author",
        on_delete=models.SET_NULL,
        null=True,
        related_name="books",
        verbose_name="автор",
    )
    summary = models.TextField(
        "описание",
        max_length=1000,
        help_text="Введите кратное описание книги",
    )
    isbn = models.CharField(
        "ISBN",
        max_length=13,
        help_text=(
            "13-значный международный "
            '<a href="https://www.isbn-international.org/content/what-isbn">код ISBN</a>'
        ),
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="books",
        help_text="Выберите жанр книги",
    )

    def __str__(self) -> str:
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.pk)])


class BookInstance(models.Model):
    LOAN_STATUS = (
        ("m", "На обслуживании"),
        ("o", "На руках"),
        ("a", "Доступна"),
        ("r", "Зарезервирована"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Уникальный ID данного экземпляра книги.",
    )
    book = models.ForeignKey(
        "Book",
        on_delete=models.SET_NULL,
        null=True,
        related_name="instances",
        verbose_name="книга",
    )
    imprint = models.CharField(
        "издательство",
        max_length=100,
    )
    due_back = models.DateField(
        "доступна после",
        null=True,
        blank=True,
    )
    status = models.CharField(
        "статус",
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text="Доступность книги",
    )

    class Meta:
        ordering = ["due_back"]

    def __str__(self) -> str:
        return f"{self.id} {self.book.title}"

    def get_absolute_url(self):
        return reverse("book-instance-detail", args=[str(self.pk)])


class Author(models.Model):
    first_name = models.CharField(
        "имя",
        max_length=100,
    )
    last_name = models.CharField(
        "фамилия",
        max_length=100,
    )
    date_of_birth = models.DateField(
        "дата рождения",
        null=True,
        blank=True,
    )
    date_of_death = models.DateField(
        "дата смерти",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.pk)])
