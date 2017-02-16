
from books.build_book_data import ScrapeGutenberg
from books.models import Author, Text, InputText, FileText
#from books.serializers import BookSerializer, AuthorSerializer
from books.forms import IDForm, InputTextForm, FileTextForm, AuthorForm
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.views import View
from django.views.generic import FormView, ListView, DetailView
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


"""
# Create your views here.
class APIBookList(APIView):
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



class APIAuthorList(APIView):

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
"""


def index(request):
    ctx = {'title':"Home"}
    return render(request, 'index.html', ctx)


class EnterIDView(View):
    """
    view for creating books from ID number
    """

    form_class = IDForm
    template_name = 'id_form.html'
    context = {'form':form_class, 'title':'Enter ID'}
    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):
        cxt = self.context.copy()
        form = self.form_class(request.POST)
        if form.is_valid():
            html_id = form['html_id']
            scrape = ScrapeGutenberg(html_id.value())
            data = scrape.return_book_info()
            book = Text(**data)

            book.save()
            #TODO add author functionality later
            #a = Author(author=data['author'], book=b)

            if scrape.title:
                cxt['message'] = 'Successfully Entered ' + scrape.title
            else:
                cxt['message'] = 'Successfully Entered book, however no title was found'
            if scrape.author != 'No Author Found':
                a = Author(author=scrape.author)
                a.save()
            return render(request, self.template_name, cxt)
        cxt['message'] = 'Failed to insert book'
        return render(request, self.template_name, cxt)

class EnterInputTextView(FormView):
    """
    view for creating books from ID number
    """
    form_class = InputTextForm
    template_name = 'id_form.html'
    success_url = '/books/'


class EnterFileTextView(FormView):
    """
    view for creating books from ID number
    """
    form_class = FileTextForm
    template_name = 'id_form.html'
    success_url = '/books/'

class EnterAuthorView(FormView):
    """
    view for entering author
    """
    form_class = AuthorForm
    template_name = 'id_form.html'
    success_url = '/books/'

class TextListView(ListView):
    """
    List input and file text books
    """
    model = Text
    template_name = 'list.html'
    context = {'title':'Available Books', 'toggle_menu':True}
    queryset = Text.objects.all() #may require custom model manager

class InputTextDetailView(DetailView):
    model = InputText




