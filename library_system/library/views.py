from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Loan
from .serializers import BookSerializer, LoanSerializer # type: ignore

class BookListView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class CheckoutView(APIView):
    def post(self, request):
        book_id = request.data.get('bookId')
        student_email = request.data.get('studentEmail')
        try:
            book = Book.objects.get(id=book_id)
            if book.stock > 0:
                book.stock -= 1
                book.save()
                Loan.objects.create(book=book, student_email=student_email)
                return Response({'message': 'Book checked out successfully'}, status=status.HTTP_200_OK)
            return Response({'message': 'Out of stock'}, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({'message': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
