from django.db import models
from django.contrib import admin
import bs4
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




class Gutenberg(Text):
    """
    Model for storing html file from project gutenberg website
    """
    #TODO seperate between
    parent_text = models.OneToOneField(FileText)
    html_id = models.IntegerField(primary_key=True)
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



admin.site.register([Text, Author, InputText, FileText, Genre])

