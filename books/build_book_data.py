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
import re
from collections import OrderedDict

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



class GetTextInfo(object):
    """
    Object for parsing html files from project gutenberg on

    """

    soup = None

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

    def get_title_and_author(self):
        """
        Go to the html title and get the book title and author
        :return:
        """
        try:
            contents = self.soup.find_all('title')[0].text
        except IndexError:
            self.author = "No Author Found"
            self.title = "No Title Found"
            return None, None
        by = contents.find('by')
        title = contents[:by - 1] #TODO Charlotte Perkins Gilman - Free Ebook, remove "free ebook" from the end
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


class ScrapeGutenberg(GetTextInfo):
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


    def get_soup(self):
        self.request = requests.get(self.url)
        self.soup = BeautifulSoup(self.request.content, 'html.parser')
        #TODO there may be a conflict with soup method and soup object

    def return_book_info(self):
        return {'html_id':self.id, 'url':self.url, 'title':self.title, 'html_file':self.html_io.read() }

    def return_author(self):
        return self.author


class ScrapeHTML(GetTextInfo):
    """
    use utilities on html file rather than web link
    """
    def __init__(self, html_text):
        self.html_text = html_text
        self.get_info()

    def get_soup(self):
        self.soup = BeautifulSoup(self.html_text, 'html.parser')


def split_by_regex(regex, text):
    """
    split apart text into chapters by regex,
    :param regex:
    :param text:
    :return: OrderedDict of chapter:text pairs
    """
    matches = re.search(regex, text, re.I)
    return matches

class SplitByRegex(object):
    """
    divide up text by regular expression
    """

    def __init__(self, regex, text):
        self.regex = re.compile(regex)
        self.text = text
        self.chapters = OrderedDict()
        self.create_chapters()
        pass



    def split_up(self):
        match = self.regex.search(self.text)
        if match == None:
            return None
        end = match.span()[1]
        if self.chapters == OrderedDict():
            self.chapters['Header'] = self.text[:match.span()[0]]
        else:
            chapter_name = match.group(0).strip() + ' ' #requires space in the end to resolve chapter name disputes
            print(chapter_name)
            if chapter_name in self.chapters.keys():
                duplicates = [k for k in self.chapters.keys() if k.startswith(chapter_name)]
                print(duplicates)
                self.chapters[chapter_name + ' - ' + str(len(duplicates))] = self.text[:match.span()[0]]
            else:
                self.chapters[chapter_name] = self.text[:matches.span()[0]] #TODO check to see if chapter already exists
        self.text = self.text[end:]
        return True

    def create_chapters(self):
        while True:
            if self.split_up() == None:
                break
        return self.chapters

if __name__ == "__main__":
    with open('testing_text.txt', 'r') as f:
        text = f.read()
    uppercase = r'\n[A-Z]+\n'
    matches = split_by_regex(uppercase, text)
    s = SplitByRegex(uppercase, text)
    pass





