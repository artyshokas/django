from django.db import models
import uuid

class Genre(models.Model):
    name = models.CharField('name', max_length=200, help_text='Enter the name of the genre')

    def __str__(self) -> str:
        return self.name


class Author(models.Model):
    first_name = models.CharField('first name', max_length=50)
    last_name = models.CharField('last name', max_length=50)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    
class Meta:
    ordering = ['last_name', 'first_name']



class Book(models.Model):
    title = models.CharField('title', max_length=255)
    summary = models.TextField('summary') # max_length nereikalingas su TextField
    isbn = models.CharField('ISBN', max_length=13, null=True, blank=True,
        help_text='<a href="https://www.isbn-international.org/content/what-isbn" target="_blank">ISBN kodas</a> consisting of 13 symbols')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    genre = models.ManyToManyField(Genre, help_text='Choose genre(s) for this book', verbose_name='genre(s)')

    def __str__(self) -> str:
        return f"{self.author} - {self.title}"


    # on_delete -- PROTECT neleis istrint autho jei turi knygu. 
    # SET_NULL knygose vietoj autor paliks null. 
    # CASCADE istrins ir knygas jei istrini autoriu
    # DO NOTHING - obviously


class BookInstance(models.Model):
    unique_id = models.UUIDField('unique ID', default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, verbose_name='book', on_delete=models.CASCADE)
    due_back = models.DateField('Due Back', null=True, blank=True)

    LOAN_STATUS = (
        ('m', "managed"),
        ('t', "taken"),
        ('a', "available"),
        ('r', "reserved"),
    )
    # loan status didz raid yra konstanta, kuria aprasom lauko viduje. tai yra ne laukas
    status = models.CharField('status', max_length=1, choices=LOAN_STATUS, default='m') # nustatom defaultini loan statusa m - managed
    # price = models.DecimalField('price', max_digits=18, decimal_places=2) #  decimal_places - kiek po kablelio

    def __str__(self) -> str:
        return f"{self.unique_id}: {self.book.title}" # mes per sasaja per modeli book, kreipiames i title. per foreign key

    class Meta:
        ordering = ['due_back']