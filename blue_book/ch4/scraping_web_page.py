import requests
import lxml.html

url = "https://www.shoeisha.co.jp/book/detail/9784798146072"


def to_html_element_object(url):
    res = requests.get(url)
    return lxml.html.fromstring(res.text)


def get_book_title_xpath(url):
    root = to_html_element_object(url)
    title_h1 = root.xpath("//*[@id='cx_contents_block']/div[1]/section/h1")
    print(title_h1[0].text)
    print(title_h1[0].tag)
    print(title_h1[0].attrib)


def get_book_contact_link_cssselector(url):
    root = to_html_element_object(url)
    contact_link = root.cssselect('#qa > p > a')
    [print(cl.attrib['href']) for cl in contact_link]


get_book_title_xpath(url)
get_book_contact_link_cssselector(url)


