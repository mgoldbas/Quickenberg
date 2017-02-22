# Metadata
__author__ = 'mgoldbas'
__date__ = '2/2/17'
__copyright__ = 'Copyright 2016 by Open Aristos, distributed under Mozilla 2.0 license.'
__license__ = 'This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.'

from books.models import Author, GutenbergID #, BookFile
from rest_framework import serializers



class GutenbergIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = GutenbergID
        fields = ('g_id',)



class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('author', )
