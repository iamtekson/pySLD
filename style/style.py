from .postgres import Pg
from .classification import Classification
import seaborn as sns
from .simpleStyle import SimpleStyle
from matplotlib.colors import rgb2hex


class Style:
    def __init__(
            self,
            style_name='style',
            fill_color='#ffffff',
            stroke_color="#333333",
            stroke_width=1,
            opacity=1,
            color_palette='cp',
            attribute_name=None,
            number_of_class=5,
            classification_method='nb'):

        self.style_name = style_name
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.opacity = opacity
        self.color_palette = color_palette

        # The schema of the table from postgresql
        self.schema = 'public'

        # The postgres connection function
        self.pg = None

    def connect_postgres(self, dbname, user='postgres', password='admin', host='localhost', port='5432'):
        self.pg = Pg(dbname, user, password, host, port)
        return self.pg

    def set_postgres_schema(self, schema):
        self.schema = schema

    def get_values_from_pg(self):
        column = self.attribute_name
        table = self.layer
        schema = self.schema
        return self.pg.get_values_from_column(column=column, table=table, schema=schema)
