import datetime
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .models import Fine, Book, Borrowing, Author, Genre, Publisher, Reservation
from .serializers import (
    AuthorSerializer,
    BorrowingSerializer,
    FineSerializer,
    PublisherSerializer,
    BookSerializer,
    GenreSerializer,
    ReservationSerializer,
    # CreateBorrowingSerializer
)
from rest_framework.permissions import IsAuthenticated
from .permissions import IsLibarianOrReadOnly,IsLibarian


# Create your views here.
class AuthorListView(generics.ListCreateAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    permission_classes = [IsLibarianOrReadOnly]

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    permission_classes = [IsLibarianOrReadOnly]

class GenreListView(generics.ListCreateAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = [IsLibarianOrReadOnly]

class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = [IsLibarianOrReadOnly]

class PublisherListView(generics.ListCreateAPIView):
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.all()
    permission_classes = [IsLibarianOrReadOnly]

class PublisherDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorSerializer
    queryset = Publisher.objects.all()
    permission_classes = [IsLibarianOrReadOnly]

class BookListView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    # permission_classes = [IsLibarianOrReadOnly,IsAuthenticated]

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [IsLibarianOrReadOnly,IsAuthenticated]


class BorrowingListView(generics.ListAPIView):
    serializer_class = BorrowingSerializer
    # permission_classes = [IsLibarianOrReadOnly,IsAuthenticated]
    # queryset=Borrowing.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Libarian").exists():
            return Borrowing.objects.all()
        return Borrowing.objects.filter(borrower=user.id)

class LendBook(generics.CreateAPIView):
    serializer_class = BorrowingSerializer
    permission_classes = [IsLibarian,IsAuthenticated]
    queryset=Borrowing.objects.all()

    def perform_create(self, serializer):
        serializer.save(libarian=self.request.user)
   
class BorrowingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BorrowingSerializer
    # queryset = Borrowing.objects.all()
    permission_classes = [IsLibarianOrReadOnly,IsAuthenticated]

    def get_queryset(self):
       
        user = self.request.user
        if user.groups.filter(name="Libarian").exists():
            return Borrowing.objects.all()
        return Borrowing.objects.filter(borrower=user.id)

    

class ReservationListView(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Libarian").exists():
            return Reservation.objects.all()
        return Reservation.objects.filter(borrower=user.id)

    def perform_create(self,serializer):
        serializer.save(user_id=self.request.user)

class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Libarian").exists():
            return Reservation.objects.all()
        return Reservation.objects.filter(borrower=user.id)


class FineListView(generics.ListCreateAPIView):
    queryset = Fine.objects.all()
    serializer_class = FineSerializer

    def get_queryset(self):
       
        user = self.request.user
        if user.groups.filter(name="Libarian").exists():
            return Fine.objects.all()
        return Fine.objects.filter(user_id==user.id)

class FineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fine.objects.all()
    serializer_class = FineSerializer

    def get_queryset(self):
       
        user = self.request.user
        if user.groups.filter(name="Libarian").exists():
            return Fine.objects.all()
        return Fine.objects.filter(user_id=user.id)

class SearchBookView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_fields = ["id","title","isbn","author","genre","edition"]



@api_view(['GET'])
@permission_classes([IsLibarian])
def books_lended_by_libarian(request):
    libarian = request.user
    lended_books = libarian.libarian.all()
    serializer = BookSerializer(data=lended_books,many=True)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated,IsLibarian])
def return_book(request,book_id):
    user = request.user
    borrowed_book = Borrowing.objects.filter(book=book_id,borrower=user,returned=False)
    borrowed_book.returned=True
    borrowed_book.return_date=datetime.datetime.now()
    borrowed_book.save()
    serializer = BorrowingSerializer(data=borrowed_book)
    return Response(data=serializer.data)
