import csv
import io

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


def create_csv():
    output = io.StringIO()
    csv_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    header = ["id", "title", "url", "writer_id", "writer_name", "mojidukai_type_id", "mojidukai_type_name"]
    csv_writer.writerow(header)

    writers = Writer.all()
    writers.load('works', 'works.mojidukai_type')
    for writer in writers:
        for work in writer.works:
            line = [
                work.id,
                work.title,
                work.build_url(),
                work.writer.id,
                work.writer.name,
                work.mojidukai_type.id,
                work.mojidukai_type.name,
            ]
            csv_writer.writerow(line)
    return output.getvalue()


if __name__ == "__main__":
    csv_str = create_csv()
    print(csv_str)