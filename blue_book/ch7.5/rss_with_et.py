"""
make RSS using xml.etree.ElementTree
"""
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Define the original namespaces
NAMESPACES = {'book': "http://example.com/xmlns/book", 'pen': "http://example.com/xmlns/pen"}


def create_rss():
    """make RSS."""
    for ns_name, ns_uri in NAMESPACES.items():
        ET.register_namespace(ns_name, ns_uri) # Register namespaces
        # This namespace url should be unique on the internet
        # Therefore to make a feed you should combine host domain and appropriate path (like /xmlns/book)

    # Make <rss> element
    elm_rss = ET.Element(
        "rss",
        attrib={
            'version': "2.0",
            'xmlns:book': NAMESPACES['book'],
        },
    )

    # Make <channel> element
    elm_channel = ET.SubElement(elm_rss, 'channel')

    # Add the sub elements of a channel element in a lump
    channel_sources = {
        'title': "芥川龍之介の新着作品",
        'link': "http://www.aozora.gr.jp/index_pages/prson879.html",
        'description': "青空文庫に追加された芥川龍之介の新着作品のフィード",
    }

    children_of_channel = []
    for tag, text in channel_sources.items():
        child_elm_of_channel = ET.Element(tag)
        child_elm_of_channel.text = text
        children_of_channel.append(child_elm_of_channel)

    # Add elements in a lump
    elm_channel.extend(children_of_channel)

    # Add <item> element: add sub elements one by one
    elm_item = ET.SubElement(elm_channel, 'item')

    # Add <item><title> element
    elm_item_title = ET.SubElement(elm_item, 'title')
    elm_item_title.text = "羅生門"

    # Add <item><link> element
    elm_item_link = ET.SubElement(elm_item, 'link')
    elm_item_link.text = "http://www.aozora.gr.jp/cards/000879/card128.html"

    # Add <item><description> element
    elm_item_description = ET.SubElement(elm_item, 'description')
    elm_item_description.text = ('<a href="http://www.aozora.gr.jp/index_pages/prson879.html">芥川</a>の５作目の短編小説。')

    # Add <item><book:writer> element
    elm_item_writer = ET.SubElement(elm_item, 'book:writer', id="879")
    elm_item_writer.text = "芥川龍之介"

    # Convert to XML strings
    xml = ET.tostring(elm_rss, 'utf-8')

    # Add <?xml version="1.0"?> to first row and reshape
    with minidom.parseString(xml) as dom:
        return dom.toprettyxml(indent="  ")


if __name__ == "__main__":
    rss_str = create_rss()
    print(rss_str)
    print("="*30)
    print(ET._namespace_map)