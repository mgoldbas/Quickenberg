# Metadata
__author__ = 'mgoldbas'
__date__ = '2/3/17'
__copyright__ = 'Copyright 2016 by Open Aristos, distributed under Mozilla 2.0 license.'
__license__ = 'This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.'


# Manage Resources
from books.views import index, EnterFileTextView, EnterInputTextView, EnterIDView, TextListView, EnterAuthorView\
    , EnterGenreView
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^books/$', TextListView.as_view(), name='books'),
    url(r'^id/$', EnterIDView.as_view(), name='add_id'),
    url(r'^file/$', EnterFileTextView.as_view(), name='add_file'),
    url(r'^input/$', EnterInputTextView.as_view(), name='add_input'),
    url(r'^author/$', EnterAuthorView.as_view(), name='add_author'),
    url(r'^genre/$', EnterGenreView.as_view(), name='add_genre'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

