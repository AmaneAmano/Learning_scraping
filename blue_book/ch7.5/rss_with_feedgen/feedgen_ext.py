"""feedgen extention namespace"""
from lxml import etree

from feedgen.ext.base import BaseExtension


class BookBaseExtension(BaseExtension):
    """book extension namespace"""

    # URL of an original namespace
    BOOK_NS = "http://exmaple.com/xmlns/book"

    def __init__(self):
        self.__writer = {}

    def extend_ns(self):
        """extension namespace"""
        return {'book': self.BOOK_NS}

    def _extend_xml(self, elm):
        """Add element"""
        if self.__writer:
            writer = etree.SubElement(
                elm,
                '{%s}Writer' % self.BOOK_NS, # {namespace url} element name
                attrib={'id': self.__writer.get('id')}  # Application id element
            )
            writer.text = self.__writer.get('name')  # Application element content
        return elm

    def writer(self, name_and_id_dict=None):
        """pass to self.__writer"""
        if name_and_id_dict is not None:
            name = name_and_id_dict.get('name')
            id_ = name_and_id_dict.get('id')
            if name and id_:
                self.__writer = {'name': name, 'id': id_}
            elif not name and not id_:
                self.__writer = {}
            else:
                raise ValueError('Set both name and id')
        return self.__writer


class BookFeedExtension(BookBaseExtension):
    """Apply to channel element"""

    def extend_rss(self, rss_feed):
        """Called when adding element"""
        channel = rss_feed[0]
        self._extend_xml(channel)


class BookEntryExtension(BookBaseExtension):
    """Apply to item element"""
    def extend_rss(self, entry):
        self._extend_xml(entry)

