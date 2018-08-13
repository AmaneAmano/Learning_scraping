import json

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

def create_json():
    works = []
    writers = Writer.all()
    writers.load('works', 'works.mojidukai_type')
    for writer in writers:
        for work in writer.works:
            d = dict()
            d['id'] = work.id
            d['title'] = work.title
            d['url'] = work.build_url()
            d['writer'] = {'id': writer.id, 'name': writer.name}
            d['mojidukai_type'] = {'id': work.mojidukai_type.id, 'name': work.mojidukai_type.name}
            works.append(d)
    return json.dumps(works, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    json_str = create_json()
    print(json_str)