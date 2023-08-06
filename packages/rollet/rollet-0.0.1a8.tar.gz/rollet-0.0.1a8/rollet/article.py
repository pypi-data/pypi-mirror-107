#!/usr/bin/env python
# coding: utf-8


__all__ = [
    'ArticleMDPI',
]


import re
from requests import get
from requests.exceptions import InvalidURL
from bs4 import BeautifulSoup as B



class Article:
    """
    Base Article crawler class
    """
    _url = re.compile(r'([\w+]+\:\/\/)?([\w\d-]+\.)*[\w-]+[\.\:]\w+([\/\?\=\&\#\.]?[\w-]+)*\/?')
    
    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            if value: setattr(self, attr, value)
            else:
                raise InvalidURL(
                    f'Provided url does not match {self._head} header. {attr} missing'
                )
    
    
    def to_dict(self):
        char = {
            k: getattr(self, k, None)
            for k in ['abstract', 'title', 'doi']
        }
        list_ = {k: getattr(self, k, []) for k in ['authors']}
        return {**char, **list_}
    


class ArticleMDPI(Article):
    """
    Crawler for mdpi.com domain
    """
    
    _head = "mdpi"
    
    def __init__(self, url: str, **kwargs) -> None:
        with get(url) as response:
            crawl = any(i for i in response.cookies.list_domains()
                        if self._head in i)
            page = B(response.text, 'html.parser').find(
                id='abstract') if crawl else None
        super().__init__(body = page)

    @property
    def abstract(self):
        return self.body.find(class_='art-abstract').text.strip()

    @property
    def title(self):
        return self.body.find(class_='title', attrs={
            'itemprop': 'name'
        }).text.strip()

    @property
    def doi(self):
        doi = None
        bib = self.body.find(class_='bib-identity')
        if len(bib.find_all('a')):
            doi = bib.find_all('a')[-1].text.strip()
        elif self._url.search(bib.text.strip()):
            doi = self._url.search(bib.text.strip()).group()
        return doi

    @property
    def authors(self):
        return list(map(
            lambda x: x.text,
            self.body.find(class_='art-authors').find_all(
                class_='sciprofiles-link__name')))


class ArticleNIH(Article):
    """
    Crawler for nih.gov domain
    """

    _head = 'pubmed'

    def __init__(self, url: str, **kwargs) -> None:
        with get(url) as response:
            crawl = any(i for i in response.cookies.list_domains()
                        if self._head in i)
            page = B(response.text, 'html.parser').find(
                id='article-details',
                class_='article-details') if crawl else None
        super().__init__(body = page)

    @property
    def abstract(self):
        return self.body.find(id='enc-abstract').text.strip()

    @property
    def title(self):
        return self.body.find('h1', class_='heading-title').text.strip()

    @property
    def doi(self):
        return self.body.find(class_='identifier doi').find(
            class_='id-link').attrs.get('href')

    @property
    def authors(self):
        return list(map(
            lambda x: x.text,
            self.body.find(class_='authors-list').find_all(
                class_='full-name')))