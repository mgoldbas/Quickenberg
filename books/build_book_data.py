# Metadata
__author__ = 'mgoldbas'
__date__ = '2/2/17'
__copyright__ = 'Copyright 2016 by Open Aristos, distributed under Mozilla 2.0 license.'
__license__ = 'This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.'


# Manage Resources

import requests
import re
from bs4 import BeautifulSoup
from io import StringIO
from django.conf import settings

def get_book_text(text):
    """
    take a book, return text data from gutenberg site
    """
    url_string = build_gutenberg_url(text)
    web_request = requests.get(url_string)
    return web_request.text

def get_book_text_with_id(id):
    text = str(id) + '-0.txt'
    return get_book_text(text)


def build_gutenberg_url(text):
    number = text[:text.find('-')]
    gutenberg_url = "https://www.gutenberg.org/files/{}/{}".format(number, text)
    return gutenberg_url

def test_get_book_test(text):
    """
    test book by url is the same as local book
    :param text:
    :return:
    """
    with open('test_texts/'+text,'r') as f:
        local_book_text = f.read()
    web_book_text = get_book_text(text)
    print(len(local_book_text))
    print(len(web_book_text))
    with open('web_text.txt', 'w') as f:
        f.write(web_book_text)
    assert local_book_text == web_book_text
    """
    doesn't work because when you write a book to text some of it gets reformatted
    """

def break_text_into_chunks(regex, text):
    """

    :param regex:
    :param text:
    :return:
    """
    book_text = get_book_text(text)




class ScrapeGutenberg:
    """
    Comprehensive object for finding all required information from Project Gutenberg pages
    """

    _url = "https://www.gutenberg.org/ebooks/{}"

    def __init__(self, id):
        self.id = id
        self.url = self._url.format(id)
        self.soup()
        self.get_info()
        pass


    def soup(self):
        self.request = requests.get(self.url)
        self.soup = BeautifulSoup(self.request.content, 'html.parser')


    def get_info(self):
        """
        master function for getting information from soup
        :return:
        """
        self.get_txt_link()
        self.get_title_and_author()
        self.get_files()

    def get_txt_link(self):
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
        if self.text_link == None:
            print(self.soup.contents)

    def get_title_and_author(self):
        try:
            contents = self.soup.find_all('title')[0].text
        except IndexError:
            self.author = "No Author Found"
            self.title = "No Title Found"
            return None, None
        by = contents.find('by')
        title = contents[:by - 1]
        author = contents[by+2:]
        self.title = title
        self.author = author
        return title, author

    def get_files(self):
        """
        get book text and store it as a file-like object
        :return:
        """

        request = requests.get(self.text_link)
        self.book_io = StringIO(request.text)
        self.html_io = StringIO(self.soup.text)

    def return_book_info(self):
        return {'html_id':self.id, 'url':self.url, 'title':self.title, 'html_file':self.html_io.read()
            , 'author':self.author}

if __name__ == "__main__":
    s = ScrapeGutenberg(6312)
    print(s.return_book_info())


