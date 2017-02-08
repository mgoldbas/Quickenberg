# Metadata
__author__ = 'mgoldbas'
__date__ = '2/3/17'
__copyright__ = 'Copyright 2016 by Open Aristos, distributed under Mozilla 2.0 license.'
__license__ = 'This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.'


# Manage Resources
from books.views import index, IDView, BookListView, EnterTextView
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^id/$', IDView.as_view(), name='add_id'),
    url(r'^text/$', EnterTextView.as_view(), name='add_text'),
    url(r'^books/$', BookListView.as_view(), name='books'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

