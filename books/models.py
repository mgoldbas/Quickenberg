from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin
from django.core.files import File
from bs4 import BeautifulSoup
import requests
from io import StringIO

from books.build_book_data import SplitByRegex

# Create your models here.




class Author(models.Model):
    """
    Model for storing Authors associated with Texts
    """
    name = models.CharField(primary_key=True, max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Text(models.Model):
    is_broken_up = models.BooleanField(default=False)
    regex = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=False)
    author = models.ManyToManyField(Author, null=True, blank=True)


    def break_up(self):
        """
        use this function to break up text
        must have a regex value
        :return:
        """
        if self.regex == None:
            raise ValueError
        self.is_broken_up = True


    def __str__(self):
        return self.title

class FileText(Text):
    """
    a class for storing text by file
    """
    words = models.FileField()
    is_gutenberg = models.BooleanField()



class InputText(Text):
    """
    a class for storing text by input
    """
    words = models.TextField()

class GutenbergID(models.Model):
    """
    Initial model for storing funtions around building gutenberg data
    """
    g_id = models.IntegerField(primary_key=True)

    valid = None

    _url = "https://www.gutenberg.org/ebooks/{}"


    def __str__(self):
        return str(self.g_id)


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """
        override save method to create Gutenberg Model upon save
        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return:
        """
        super(GutenbergID, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        self.url = self._url.format(self.g_id)
        self.set_info()

    def setup_validity(self):
        self.valid = True
        self.errors = []

    def set_invalid(self, error):
        self.errors.append(error)
        self.valid = False

    def is_valid(self):
        return self.valid

    def set_info(self):
        """
        master function for getting information from soup
        :return:
        """
        self.setup_valid()
        self.set_txt_link()
        self.set_author()
        self.set_files()

    def set_soup(self):
        self.request = requests.get(self.url)
        self.soup = BeautifulSoup(self.request.content, 'html.parser')

    def get_soup(self):
        return self.soup

    def set_txt_link(self):
        """
        get the text link
        :return:
        """
        self.text_link = None
        for s in self.soup.find_all('a', href=True):
            link = s['href']
            if link.endswith('.txt') or link.endswith('.txt.utf-8'):
                self.text_link = link
                self.text_link = 'http:' + self.text_link
                self.set_valid()
        if self.text_link is None:
            self.set_invalid('No Text Link')

    def set_author_and_title(self):
        """
        Go to the html title and get the book title and author
        :return:
        """
        try:
            contents = self.soup.find_all('title')[0].text
        except IndexError:
            self.set_invalid('No Title and Author Found')
            return None, None
        by = contents.find('by')
        title = contents[:by - 1] #TODO seperate get author from set author
        author = contents[by+2:]
        dash = author.find('-')
        if dash > 0:
            author = author[:dash]
        self.title = title
        self.author = author

    def get_author(self):
        return self.author

    def get_title(self):
        return self.title

    def set_files(self):
        """
        get book text and store it as a file-like object
        :return:
        """

        request = requests.get(self.text_link)
        print('Length of request.text is ', str(len(request.text)))
        string_io = StringIO(request.text)
        print(string_io)
        print(dir(string_io))
        self.book_io = File(string_io)

        if self.book_io is None:
            self.set_invalid('Book Object is None')
        self.html_io = File(StringIO(self.soup.text))
        if self.html_io is None:
            self.set_invalid('HTML object is None')

    def get_book_file(self):
        return self.book_io

    @property
    def get_html_file(self):
        return self.html_io



class Gutenberg(Text):
    """
    Model for storing html file from project gutenberg website
    """
    parent_text = models.OneToOneField(FileText)
    html_id = models.OneToOneField(GutenbergID)
    url = models.URLField(default='http://www.gutenberg.org/cache/epub/1232/pg1232.txt') #the prince is the default
    html_file = models.FileField()


    def __str__(self):
        return self.title

    def get_soup(self):
        return bs4.BeautifulSoup(self.html_file.read())


    class Meta:
        ordering = ('title',)




class Chapter(models.Model):
    """
    Parent model for chapters
    """
    number = models.DecimalField(decimal_places=1, max_digits=3)
    chapter = models.TextField()

    class Meta:
        ordering = ('number',)

class InputChapter(Chapter):
    """
    a model for storing chapters from input text model
    """
    source = models.ForeignKey(InputText)

class FileChapter(Chapter):
    """
    a model for storing chapters from file text model
    """
    source = models.ForeignKey(FileText)


class Genre(models.Model):
    """
    Genre for models
    """
    fiction = models.BooleanField()
    genre = models.CharField(max_length=100)
    text = models.ManyToManyField(Text, null=True)





admin.site.register([Text, Author, InputText, FileText, Genre, GutenbergID])

