from django.urls import path
from .views import (
    BookDetailView,
    BookListView,
    AuthorDetailView,
    AuthorListView,
    PublisherListView,
    PublisherDetailView,
    FineListView,
    FineDetailView,
    BorrowingDetailView,
    BorrowingListView,
    GenreDetailView,
    GenreListView,
    ReservationDetailView,
    ReservationListView,
    SearchBookView,
    LendBook,
    books_lended_by_libarian,
    return_book
)

urlpatterns = [
    path("authors/", AuthorListView.as_view(), name="authors"),
    path("authors/<int:pk>", AuthorDetailView.as_view(), name="author-detail"),
    path("publishers/", PublisherListView.as_view(), name="publishers"),
    path("publishers/<int:pk>", PublisherDetailView.as_view(), name="publisher-detail"),
    path("books/", BookListView.as_view(), name="books"),
    path("books/<int:pk>", BookDetailView.as_view(), name="book-detail"),
    path("fines/", FineListView.as_view(), name="fines"),
    path("fines/<int:pk>", FineDetailView.as_view(), name="fine-detail"),
    path("genres/", GenreListView.as_view(), name="genres"),
    path("genres/<int:pk>", GenreDetailView.as_view(), name="genre-detail"),
    path("reservations/", ReservationListView.as_view(), name="reservations"),
    path("reservations/<int:pk>", ReservationDetailView.as_view(), name="reservation-detail"),
    path("borrowings/", BorrowingListView.as_view(), name="borrowings"),
    path("borrowings/<int:pk>", BorrowingDetailView.as_view(), name="borrowing-detail"),
    path("lend-book/", LendBook.as_view(), name="lend-book"),
    path("books-search",SearchBookView.as_view(),name="search-books"),
    path("libarian/lended-books",books_lended_by_libarian,name="books_lended_by_libarian"),
    path("borrowed-books/return-book/<int:book_id",return_book,name="return-book"),

]
