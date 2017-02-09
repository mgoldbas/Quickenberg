from django.db import models
from django.contrib import admin
import bs4
from books.build_book_data import SplitByRegex

# Create your models here.



class Book(models.Model):
    """
    Main class for storing text data
    """
    #TODO seperate between
    html_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200, null=True)
    url = models.URLField(default='http://www.gutenberg.org/cache/epub/1232/pg1232.txt') #the prince is the default
    regex_seperator = models.CharField(max_length=100, null=True)
    html_file = models.FileField()


    def __str__(self):
        return self.title

    def get_soup(self):
        return bs4.BeautifulSoup(self.html_file.read())


    class Meta:
        ordering = ('title',)



class Author(models.Model):
    author = models.CharField(primary_key=True, max_length=300)
    books = models.ManyToManyField('Book')

    def __str__(self):
        self.author

    class Meta:
        ordering = ('author',)



class BookFile(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    file = models.FileField()

    def make_chapters(self, regex):
        """
        chop up book in to chapters
        :return:
        """
        split = SplitByRegex(regex, self.file.read())
        for k, v in split.chapters.items():
            book_chapter = BookChapter(chapter=k, book=self, text=v)
            book_chapter.save()

class BookChapter(models.Model):
    chapter = models.CharField(max_length=200)
    book = models.ForeignKey(BookFile, on_delete=models.CASCADE)
    text = models.TextField()


admin.site.register([Book, Author, BookFile, BookChapter])

