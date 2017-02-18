
from books.build_book_data import ScrapeGutenberg
from books.models import Author, Text, InputText, FileText, Genre
#from books.serializers import BookSerializer, AuthorSerializer
from books.forms import IDForm, InputTextForm, FileTextForm, AuthorForm, GenreForm, GutenbergForm

from django.contrib import messages
from django.views import View
from django.views.generic import FormView, ListView, DetailView
from django.shortcuts import render
from itertools import chain
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


class EnterIDView(FormView):
    """
    view for creating books from ID number
    """

    form_class = IDForm
    template_name = 'id_form.html'
    success_url = '/id/'

    def get_context_data(self, **kwargs):
        context = super(EnterIDView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            html_id = form['html_id']
            print(html_id)
            scrape = ScrapeGutenberg(html_id.value())
            author, title = scrape.get_title_and_author()
            author_form = AuthorForm(data={'name':author})
            if author_form.is_valid():
                author_form.save()
            file_text_form = FileTextForm(data=scrape.make_book())
            if file_text_form.is_valid():
                file_text_form.save()
            gutenberg_form = GutenbergForm(data=scrape.make_gutenberg())
            if gutenberg_form.is_valid():
                gutenberg_form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


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


class EnterAuthorView(FormView, ListView):
    """
    view for entering author
    """
    form_class = AuthorForm
    template_name = 'author.html'
    success_url = '/author/'
    queryset = Author.objects.all()
    context_object_name = 'authors'

    def form_valid(self, form):
        form.save()
        return super(EnterAuthorView, self).form_valid(form)

    def form_invalid(self, form):
        response = super(EnterAuthorView, self).form_invalid(self, form)
        messages.error(response, 'Did not enter valid author')
        return response

class EnterGenreView(FormView, ListView):
    """
    View for creating new genres to associate with book
    """
    form_class = GenreForm
    template_name = 'author.html'
    success_url = '/genre/'
    queryset = Genre.objects.all()
    context_object_name = 'authors'

class TextListView(ListView):
    """
    List input and file text books
    """
    template_name = 'book_list.html'
    queryset = list(chain(InputText.objects.all(), FileText.objects.all())) #may require custom model manager
    context_object_name = 'books'


class InputTextDetailView(DetailView):
    model = InputText




