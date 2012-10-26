from bs4 import BeautifulSoup
import requests
from urlparse import urljoin

KNESSET_BASE_URL = 'http://www.knesset.gov.il/mk/heb/'
KNESSET_URL = urljoin(KNESSET_BASE_URL, 'MKIndex_Current.asp?view=4')

class KnessetException(Exception):
    pass

class KnessetScraper(object):
    @staticmethod
    def in_hebrew(string):
        # If the string is Unicode (wrongly), convert it to a string of bytes first
        string = ''.join([chr(ord(ch)) for ch in string])

        # Decode it to Unicode with the correct Hebrew code page
        return string.decode('cp1255')

    def __init__(self, td_ministers, td_deputies):
        self.td_ministers = td_ministers
        self.td_deputies = td_deputies

    def scrape_member(self, link):
        div = link.parent

        classes = div.attrs.get('class', [])
        if 'MKIconM' in classes:
            member_type = u'male_mk'
        elif 'MKIconF' in classes:
            member_type = u'female_mk'
        elif 'MKIconNotMK' in classes:
            member_type = u'not_mk'
        else:
            raise KnessetException("Malformed government member")

        member_name = self.in_hebrew(link.text)

        spans = div('span')
        if len(spans) > 1:
            raise KnessetException("Malformed government member")

        if spans:
            span = spans[0]
            member_description = self.in_hebrew(span.text)
        else:
            member_description = u''

        td = [p for p in div.parents if p.name == 'td'][0]
        if td == self.td_ministers:
            member_rank = u'minister'
        elif td == self.td_deputies:
            member_rank = u'deputy'
        else:
            raise KnessetException("Malformed government member")

        member_link = urljoin(KNESSET_BASE_URL, link.get('href'))

        return {
            'type' : member_type,
            'rank' : member_rank,
            'name' : member_name,
            'description' : member_description,
            'link' : member_link
        }

    @classmethod
    def scrape(cls):
        r = requests.get(KNESSET_URL)
        r.raise_for_status()

        soup = BeautifulSoup(r.text)
        tds = soup('td', { 'class' : 'DataText' })

        if len(tds) != 2:
            raise KnessetException("Error finding DataText table cells")

        scraper = KnessetScraper(td_ministers=tds[0], td_deputies=tds[1])

        member_links = soup('a', { 'class' : 'DataText' })
        return [ scraper.scrape_member(link) for link in member_links ]
