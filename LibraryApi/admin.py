from django.contrib import admin

# Register your models here.
from .models import Book,Borrowing,Genre,Author,Publisher,Fine,Reservation

admin.site.register(Book)
admin.site.register(Borrowing)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Fine)
admin.site.register(Reservation)
admin.site.register(Genre)

