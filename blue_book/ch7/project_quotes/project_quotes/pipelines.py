# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from hashlib import sha256

from orator import DatabaseManager, Model
from orator.orm import belongs_to_many

from project_quotes.settings import ORATOR_CONFIG


db = DatabaseManager(ORATOR_CONFIG)
Model.set_connection_resolver(db)


class Quote(Model):
    """
    quotes table model
    """
    @belongs_to_many
    def tags(self):
        return tag


class Tag(Model):
    """
    tags table model
    """
    @belongs_to_many
    def quote(self):
        return Quote


class DatabasePipeline(object):
    """
    Save Quotes to MySQL
    """
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        """process each items"""
        self.items.append(item)
        return item

    def close_spider(self, spider):
        """process when spider finish"""
        for item in self.items:
            text_hash = sha256(
                item['text'].encode('utf8', 'ignore')).hexdigest()
            exist_quote = Quote.where('text_hash', text_hash).get()
            if exist_quote:
                continue
            quote = Quote()
            quote.author = item['author']
            quote.text = item['text']
            quote.text_hash = text_hash
            quote.save()

            tags = []

            for tag_name in item['tags']:
                tag = Tag.where('name', tag_name).first()
                if not tag:
                    tag = Tag()
                    tag.name = tag_name
                    tag.save()
                tags.append(tag)
                quote_tags = quote.tags()
                quote_tags.save(tag)