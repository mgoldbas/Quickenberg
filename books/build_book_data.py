# Metadata
__author__ = 'mgoldbas'
__date__ = '2/2/17'
__copyright__ = 'Copyright 2016 by Open Aristos, distributed under Mozilla 2.0 license.'
__license__ = 'This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.'


# Manage Resources

import requests
import re
from bs4 import BeautifulSoup



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

    def get_txt_link(self):
        """
        get the text link
        :return:
        """
        for s in self.soup.find_all('a', href=True):
            link = s['href']
            if link.endswith('.txt'):
                self.text_link = link

    def get_title_and_author(self):
        contents = self.soup.find_all('h1')#[0].contents[0]
        print(contents)
        by = contents.find('by')
        title = contents[by:]
        print(title)
        author = contents[:by+2]
        print(author)



if __name__ == "__main__":
    ScrapeGutenberg(5776)


