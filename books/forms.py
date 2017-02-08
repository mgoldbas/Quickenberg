# Metadata
__author__ = 'mgoldbas'
__date__ = '2/6/17'
__copyright__ = 'Copyright 2016 by Open Aristos, distributed under Mozilla 2.0 license.'
__license__ = 'This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.'


# Manage Resources
from django import forms
from books.models import Book



# Classes

class IDForm(forms.Form):
    html_id = forms.IntegerField()

class TextForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ()

