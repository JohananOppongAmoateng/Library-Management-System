from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book,Borrowing,Genre,Author,Publisher,Fine,Reservation


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    class Meta:
        model = User
        fields = ["username","email"]
        

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    author = AuthorSerializer(many=True)
    class Meta:
        model = Book
        fields = "__all__"

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        genre_data = validated_data.pop('genre')
        book = Book.objects.create(**validated_data)

        # for author in author_data:
        author_obj = Author.objects.create(**author_data)
        book.author.add(author_obj)

        # for genre in genre_data:
        genre_obj = Genre.objects.create(**genre_data)
        print(genre_obj)
        book.genre.add(genre_obj)

        return book

    

class BorrowedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title","isbn","edition"]


    
class BorrowingSerializer(serializers.ModelSerializer):
    due_date = serializers.DateTimeField(read_only=True)
    borrower= UserSerializer()
    libarian = UserSerializer(read_only=True)
    book = BorrowedBookSerializer()

    class Meta:
        model = Borrowing
        fields = "__all__"
        


    def create(self, validated_data):
        borrower_data = validated_data.pop('borrower')
        print(borrower_data)
        book = validated_data.pop('book')
                    
        # borrower = User.objects.get(**borrower_data)
        book = Book.objects.get(**book)
        if book.available:
            user = User.objects.get(username=borrower_data['username'])         
            
            lent_book = Borrowing.objects.create(**validated_data,book=book,borrower=user)
            book.available = False
            book.save()

            return lent_book

    
    # def update()
        
        

class ReservationSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    book_id = BookSerializer()
    class Meta:
        model = Reservation
        fields = "__all__"

class FineSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    borrowing_id = BorrowingSerializer()
    class Meta:
        model = Fine
        fields = "__all__"