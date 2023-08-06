
__all__ = [
    "BaseExtractor"
]

import re
from requests import get
from requests.exceptions import InvalidURL
from bs4 import BeautifulSoup as B
from tldextract import extract
from html import unescape
from json import loads
from pprint import pprint as cat
from datetime import datetime


from rollet import settings


class BaseExtractor:
    def __init__(self, url, **kwargs):
        """
        Create BaseExtractor instance
        url: string
        timeout: float, request timeout. Default 1 sec.
        abstract_**kwargs: **kwargs for abstract fetch
        title_**kwargs: **kwargs for title fetch
        """
        
        self.url = url
        self.domain = extract(url).domain
        self.date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self._scrap(**kwargs)
        self._init_kwargs(**kwargs)
    
    def _scrap(self, **kwargs):
        timeout = kwargs.get('timeout', 1)
        with get(self.url, timeout = timeout) as response:
            self._status = response.status_code
            self._header = response.headers
            self._page = B(response.text, 'html.parser')
    
    def _init_kwargs(self, **kwargs):
        self._abstract_kwargs, self._title_kwargs, self._lang_kwargs = {}, {}, {}
        for k,v in kwargs.items():
            field, key = k.split('__')
            if field == 'abstract': self._abstract_kwargs.update({key:v})
            elif field == 'title': self._title_kwargs.update({key:v})
            elif field == 'lang': self._lang_kwargs.update({key:v})
    
    
    @staticmethod
    def _get_content(tag, **kwargs):
        """
        Get content from element Tag
        tag: bs4.element.Tag
        script_keys: List, of keys if tag is script
        attr: str, key attribute if tag is neither a meta nor a script
        :return: content
        """

        def _finditem(obj, key):
            """
            Find key recursively in dict
            obj: Dict
            key: str
            :return: None or dict item
            """
            if key in obj: return obj[key]
            for k, v in obj.items():
                if isinstance(v, dict):
                    item = _finditem(v, key)
                    if item is not None:
                        return item

        if tag.name == 'meta':
            content = tag.attrs.get('content', [])
        elif tag.name == 'script':
            keys = kwargs.get('script_keys', [])
            try:
                serie = loads(tag.content[0])
            except:
                content = list()
            else:
                content = [_finditem(serie, key) for key in keys]
        elif kwargs.get('attr'):
            content = tag.attrs.get(kwargs.get('attr'))
        else:
            content = tag.text.strip().replace('\n', '')

        content = content[0] if isinstance(content, list) and len(content) else content
        content = unescape(content) if isinstance(content, str) else content
        return content
    
    def fetch(self, selectors, which='first', **kwargs):
        content = list()
        arg_w = ('first', 'min', 'max')
        if which not in arg_w:
            raise ValueError(f'which should be one of {arg_w}')
        for s in selectors:
            contents_ = list()
            tags = self._page.select(s)
            if len(tags): contents_ = [self._get_content(tag, **kwargs) for tag in tags]
            if len(contents_) and which == 'first': 
                content = [contents_[0]]
                break
            else:
                try: content += ['. '.join(set(contents_))]
                except: pass
        content = content if len(content) else [None]
        if which == 'max': content = max(content, key=lambda x: len(str(x)))
        else: content = min(content, key=lambda x: len(str(x)))
        return content
    
    @property
    def title(self):
        return self.fetch(settings.TITLE, **self._title_kwargs)
    
    @property
    def abstract(self):
        return self.fetch(settings.ABSTRACT, **self._abstract_kwargs)
    
    @property
    def lang(self):
        return self._page.html.get('lang', None)
    
    @property
    def content_type(self):
        if self.url[-3:] == 'pdf': content = 'pdf'
        else:
            charset = self._header.get('Content-Type', '')
            content = re.findall('(html|pdf|json|xml)', charset)
            content = content[0] if len(content) else 'html'
        return content
    
    def to_dict(self):
        return {
            'url': self.url,
            'status': self._status,
            'title': self.title,
            'abstract': self.abstract,
            'lang': self.lang,
            'content_type': self.content_type,
            'date': self.date
        }
    
    def to_list(self, *args):
        if len(args): listed = [getattr(self, arg, None) for arg in args]
        else: listed = list(self.to_dict().values())
        return listed