
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
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
    gutenberg_id = models.IntegerField(primary_key=True, verbose_name='Gutenberg ID')

    _valid = None

    _url = "https://www.gutenberg.org/ebooks/{}"


    def __str__(self):
        return str(self.gutenberg_id)

    @property
    def get_url(self):
        return self.url

    @property
    def get_html_file(self):
        return self.html_io

    @property
    def get_book_file(self):
        return self.book_io

    @property
    def get_author(self):
        return self.author

    @property
    def get_title(self):
        return self.title

    @property
    def get_soup(self):
        return self.soup


    def set_soup(self):
        self.html_file.seek(0)
        self.soup = BeautifulSoup(self.html_file.read())

    def setup_validity(self):
        self._valid = True
        self.errors = []

    def is_valid(self):
        return self.valid

    def set_invalid(self, error):
        """
        add error to errors list and set validity to false
        :param error:
        :return:
        """
        self.errors.append(error)
        self._valid = False



    def set_info(self):
        """
        master function for getting information from soup
        :return:
        """
        self.setup_validity()
        self.set_url()
        self.set_soup()
        self.set_txt_link()
        self.set_author_and_title()
        self.set_files()


    def set_title_tag(self):
        """
        Find the title tag in the html file, usually its "Metamorphisis by Franz Kafka"
        thus seperate at "by"
        :return:
        """
        try:
            self.title_tag = self.soup.find_all('title')[0].text
            self.by_position = self.title_tag.find('by')
        except IndexError:
            self.set_invalid('No Title and Author Found')
            return


    @property
    def get_title(self):
        return self.title

    def set_title(self):
        self.title = self.title_tag[:self.by_position - 1]

    @property
    def get_author(self):
        return self.author

    def set_author(self):
        self.author =  self.title_tag[self.by_position+2:]
        dash = self.author.find('-')
        if dash > 0:
            self.author = self.author[:dash]


    def set_author_and_title(self):
        """
        Go to the html title and get the book title and author
        must set title tag prior to setting author and title
        :return:
        """
        self.set_title_tag()
        self.set_title()
        self.set_author()


    def set_html_io(self):
        """
        get book text and store it as a file-like object
        :return:
        """
        html_string_io = StringIO(self.soup.text)
        html_string_io.seek(0, 2)
        self.html_io = InMemoryUploadedFile(html_string_io, 'html_file', self.title + ' html file', None, html_string_io.tell() , None)

    @property
    def get_url(self):
        return self.url

    def set_url(self):
        self.url = self._url.format(self.gutenberg_id)

    def create_gutenberg(self): #TODO deprciate and use Form and errors for proper ingestion
        self.set_info()
        data = dict(html_number=self, url=self.url, html_file=self.html_io)
        from books.forms import GutenbergForm
        g  = Gutenberg(**data)
        g.save()


        gutenberg = GutenbergForm(data=data)
        if gutenberg.is_valid():
            gutenberg.save()
            return 'Success'
        else:
            return gutenberg.errors

    def create_author(self):
        from books.forms import AuthorForm
        a = AuthorForm(**{'name':self.author})



"""
        LEFTOVER FROM set title and author
                try:
                    contents = self.soup.find_all('title')[0].text
                except IndexError:
                    self.set_invalid('No Title and Author Found')
                    return
                by = contents.find('by')
                title = contents[:by - 1]
                author = contents[by+2:]
                dash = author.find('-')
                if dash > 0:
                    author = author[:dash]
                self.title = title
                self.author = author
        """


class Gutenberg(models.Model):
    """
    Model for storing html file from project gutenberg e
    """

    parent_text = models.OneToOneField(FileText, null= True, on_delete=models.CASCADE)
    html_number = models.OneToOneField(GutenbergID, on_delete=models.CASCADE)
    url = models.URLField(default='http://www.gutenberg.org/cache/epub/1232/pg1232.txt') #the prince is the default
    html_file = models.FileField()

    @property
    def get_soup(self):
        return self.soup

    def set_soup(self):
        self.html_file.seek(0)
        self.soup = BeautifulSoup(self.html_file.read())

    @property
    def get_book_io(self):
        return self.book_io

    def set_book_io(self):
        """
        set the book_io attribute as in memory file field for html_file
        :return:
        """
        request = requests.get(self.text_link)
        string_io = StringIO(request.text)
        string_io.seek(0, 2)
        self.book_io = InMemoryUploadedFile(string_io, 'text', 'words', None, len(request.text), None)

    @property
    def get_txt_link(self):
        return self.get_txt_link

    def set_txt_link(self):
        """
        set the text link from beautiful soup attribute
        :return:
        """
        self.text_link = None
        for s in self.soup.find_all('a', href=True):
            link = s['href']
            if link.endswith('.txt') or link.endswith('.txt.utf-8'):
                self.text_link = link
                if not self.text_link.startswith('http:'):
                    self.text_link = 'http:' + self.text_link
        if self.text_link is None:
            self.set_invalid('No Text Link')


    def create_file_text(self):
        data = {'is_gutenberg':True, }
        f = FileText(**data)





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





admin.site.register([Text, Author, InputText, FileText, Genre, GutenbergID, Gutenberg])

