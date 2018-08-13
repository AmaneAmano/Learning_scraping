import xml.etree.ElementTree as ET
from xml.dom import minidom
import logging

from orator import DatabaseManager, Model
from orator.orm import belongs_to, has_many

logger = logging.getLogger('orator.connection.queries')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    'It took %(elapsed_time)sms to execute the query %(query)s'
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)

# MySQL connection settings
config = {
    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'aozora_bunko',
        'user': 'root',
        'password': 'Qt2ZhGWQ',
        'prefix': '',
        'log_queries': True,
    }
}

db = DatabaseManager(config)
Model.set_connection_resolver(db)


class MojidukaiType(Model):
    pass


class Work(Model):
    URL_FORMAT = "http://www.aozora.gr.jp/cards/{writer_id:06d}/card{id}.html"

    @belongs_to
    def mojidukai_type(self):
        return MojidukaiType

    @belongs_to
    def writer(self):
        return Writer

    def build_url(self):
        return self.URL_FORMAT.format(
            writer_id=self.writer_id,
            id=self.id
        )


class Writer(Model):
    @has_many
    def works(self):
        return Work


def create_xml():
    elm_root = ET.Element("catalog")
    writers = Writer.all()
    writers.load('works', 'works.mojidukai_type')
    for writer in writers:
        for work in writer.works:
            elm_work = ET.SubElement(elm_root, "work", id=str(work.id))
            ET.SubElement(elm_work, "writer", id=str(writer.id)).text = writer.get_connection_name()
            ET.SubElement(elm_work, "title").text = work.title
            ET.SubElement(elm_work, "mojidukai_type", id=str(work.mojidukai_type)).text = work.mojidukai_type.name
            ET.SubElement(elm_work, "url").text = work.build_url()

    with minidom.parseString(ET.tostring(elm_root, 'utf-8')) as dom:
        return dom.toprettyxml(indent="    ")


if __name__ == "__main__":
    xml_str = create_xml()
    print(xml_str)