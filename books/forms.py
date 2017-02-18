# Metadata
__author__ = 'mgoldbas'
__date__ = '2/6/17'
__copyright__ = 'Copyright 2016 by Open Aristos, distributed under Mozilla 2.0 license.'
__license__ = 'This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.'


# Manage Resources
from django import forms
from books.models import InputText, FileText, Author, Genre, Gutenberg



# Classes
class IDForm(forms.Form):
    """
    Form that will scrape data from project gutenberg site
    """
    html_id = forms.IntegerField()



class InputTextForm(forms.ModelForm):
    """
    form for creating text by input
    """
    class Meta:
        model = InputText
        exclude = ('is_broken_up','regex',)


class FileTextForm(forms.ModelForm):
    """
    form for creating text by file
    """
    class Meta:
        model = FileText
        exclude = ('is_broken_up','regex','is_gutenberg', 'author')


class AuthorForm(forms.ModelForm):
    """
    form for creating Authors
    """
    class Meta:
        model = Author
        exclude = ()


class GenreForm(forms.ModelForm):
    """
    form for creating Genres
    """
    class Meta:
        model = Genre
        exclude = ('text',)

class GutenbergForm(forms.ModelForm):
    """
    form for creating Gutenberg objects
    """
    class Meta:
        model = Gutenberg
        exclude = ()

