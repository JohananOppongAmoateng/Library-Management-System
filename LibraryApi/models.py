from django.db import models
from django.contrib.auth import get_user_model
import datetime



# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.ManyToManyField(Author)
    title = models.CharField(max_length=255)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=20)
    edition = models.SmallIntegerField()
    genre = models.ManyToManyField(Genre)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Borrowing(models.Model):
    borrower = models.ForeignKey(get_user_model(),on_delete=models.PROTECT,related_name="borrower")
    libarian = models.ForeignKey(get_user_model(),on_delete=models.PROTECT,related_name="libarian")
    book = models.ForeignKey(Book,on_delete=models.PROTECT)
    borrowing_date = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(default=datetime.datetime.now()+ datetime.timedelta(days=3))
    returned = models.BooleanField(default=False)
    return_date = models.DateTimeField()

    def __str__(self):
        return f"{self.borrower} borrowed {self.book}"

class Reservation(models.Model):
    user_id = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book,on_delete=models.PROTECT)
    reservation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_id} reserved {self.book}"

class Fine(models.Model):
    user_id = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    borrowing_id = models.ForeignKey(Borrowing,on_delete=models.PROTECT)
    fine_amount = models.DecimalField(max_digits=6,decimal_places=2)
    fine_date = models.DateTimeField(auto_now=True)
    fine_paid_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_id} fined {self.fine_amount} for {self.borrowing_id}"
