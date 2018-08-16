"""Output the new contents of Ryunosuke Akutagawa in Aozora Bunko using feedgen"""
from feedgen.feed import FeedGenerator

from feedgen_ext import BookEntryExtension, BookFeedExtension


def create_feed():
    """Create RSS feed"""

    # For storing feed data
    fg = FeedGenerator()

    # Register the original namespace and apply the extension class of the original namespace
    fg.register_extension(
        'book',
        extension_class_feed=BookFeedExtension,
        extension_class_entry=BookEntryExtension,
    )

    # <channel><title> element
    fg.title("芥川龍之介の新着作品")
    # <channel><link> element
    fg.link(href="http://www.aozora.gr.jp/index_pages/person879.html")
    # <channel><description> element
    fg.description("青空文庫に追加された芥川龍之介の新着作品のフィード")

    # Add <channel><item> element
    fe = fg.add_entry()
    # <channel><item><title> element
    fe.title("羅生門")
    # <channel><item><link> element
    fe.link(href="http://www.aozora.gr.jp/cards/000879/card128.html")
    # <channel><item><description> element
    fe.description('<a href="http://www.aozora.gr.jp/index_pages/person879.html">芥川</a>の5作目の短編小説。')
    # <channel><item><book:writer> element
    fe.book.writer({'name': "芥川龍之介", 'id': "879"})

    return fg.rss_str(pretty=True)


if __name__ == "__main__":
    rss_str = create_feed()
    print(rss_str.decode())