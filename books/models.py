from django.db import models
from django.contrib import admin

# Create your models here.



class Book(models.Model):
    title = models.CharField(primary_key=True, max_length=200)
    url = models.URLField(default='http://www.gutenberg.org/cache/epub/1232/pg1232.txt') #the price is the default
    regex_seperator = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title

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
    book_title = models.ForeignKey(Book, on_delete=models.CASCADE)
    file = models.FileField()

class BookChapter(models.Model):
    chapter = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()


admin.site.register([Book, Author, BookFile, BookChapter])

class GutenbergID(models.Model):
    id = models.IntegerField(primary_key=True)

