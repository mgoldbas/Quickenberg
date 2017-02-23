
from books.build_book_data import ScrapeGutenberg
from books.models import Author, Text, InputText, FileText, Genre, GutenbergID
from books.serializers import GutenbergIDSerializer #, BookSerializer, AuthorSerializer
from books.forms import IDForm, InputTextForm, FileTextForm, AuthorForm, GenreForm, GutenbergForm, ModelIDForm

from django.contrib import messages
from django.core.files import File
from django.views import View
from django.views.generic import FormView, ListView, DetailView
from django.shortcuts import render
from itertools import chain
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListCreateAPIView
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


class APIGutenbergIDView(ListCreateAPIView):
    """
    View for creating books by id via URL
    """
    serializer_class = GutenbergIDSerializer
    queryset = GutenbergID.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print(help(serializer))

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



def index(request):
    ctx = {'title':"Home"}
    return render(request, 'index.html', ctx)


class EnterIDView(FormView):
    """
    view for creating books from ID number
    """

    form_class = ModelIDForm
    template_name = 'id_form.html'
    success_url = '/id/'

    def get_context_data(self, **kwargs):
        context = super(EnterIDView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.save()
        return super(EnterIDView, self).form_valid(form)


    """
    def post(self, request, *args, **kwargs):
        Use the request and scrape objects to create a new Author if that Author does not exist already,
        :param request:
        :param args:
        :param kwargs:
        :return:
        form = self.get_form()
        if form.is_valid():
            html_id = form['html_id']
            scrape = ScrapeGutenberg(html_id.value())
            if not scrape.is_valid:
                for error in scrape.errors:
                    messages.error(request, error)
                    return self.form_invalid(form)
            author = scrape.get_author()
            author_form = AuthorForm(data={'name':author})
            file_text_data = scrape.make_book()
            if author_form.is_valid():
                author_form.save()
                file_text_data['author'] = author_form.data.get('author')

            else:
                messages.error(request, 'Author was not found')
                del file_text_data['author']
            file_text_data['words'].open()
            file_text_form = FileTextForm(data=file_text_data)
            if file_text_form.is_valid():
                file_text_form.save()
            else:
                for error in file_text_form.errors:
                    messages.error(request, error + ' file text')
            gutenberg_form = GutenbergForm(data=scrape.make_gutenberg())
            if gutenberg_form.is_valid():
                gutenberg_form.save()
            else:
                for error in gutenberg_form.errors:
                    messages.error(request, error + ' gutenberg')

            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    """

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
        response = super(EnterAuthorView, self).form_invalid(form)
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




