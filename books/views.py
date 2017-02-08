
from books.build_book_data import ScrapeGutenberg
from books.models import Book, BookFile, Author
from books.serializers import BookSerializer, AuthorSerializer
from books.forms import IDForm
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.views import View
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



# Create your views here.
class APIBookList(APIView):
    """
    Get and list all books, store books in db
    """
    def get(self, request, format=None):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIBookDetail(APIView):
    """
    Get Book and list available chapters
    """
    def get_book(self, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        book = self.get_book(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        book = self.get_book(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class AuthorList(APIView):
    """
    Get and list all Authors, store Authors in db
    """
    def get(self, request, format=None):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    ctx = {}
    return render(request, 'index.html', ctx)


class IDView(View):
    """
    view for creating books from ID number
    """

    form_class = IDForm
    template_name = 'id_form.html'
    def get(self, request):
        return render(request, self.template_name, {'form':self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            html_id = form['html_id']
            scrape = ScrapeGutenberg(html_id.value())
            data = scrape.return_book_info()
            b = Book(**data)
            a = Author(author=data['author'], book=b)
            b.save()
            return render(request, self.template_name, {'form':self.form_class, 'message':'success'})
        return render(request, self.template_name, {'form':self.form_class, 'message':'failed'})


class BookListView(View):
    """
    List books
    """
    template_name = 'list.html'
    def get(self, request):
        books = Book.objects.all()
        return render(request, self.template_name, {'books':books})

    


