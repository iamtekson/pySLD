import random
from .postgres import Pg
from .classifiedStyle import ClassifiedStyle
from .rasterStyle import RasterStyle
from matplotlib.colors import rgb2hex
from .support import str_to_num


class Style (ClassifiedStyle, RasterStyle,  Pg):
    def __init__(
            self,
            attribute_name=None,
            values=None,
            number_of_class=5,
            color_palette="Spectral_r",
            style_name='style',
            geom_type='polygon',
            classification_method='natural_break',
            fill_color='#ffffff',
            stroke_color="#333333",
            stroke_width=1,
            opacity=1,

            dbname=None,
            user='postgres',
            password='admin',
            host='localhost',
            port='5432',
            schema='public',
            pg_table_name=None,

            point_size=6,
            well_known_name='circle',
            point_rotation=0,
            stroke_linecap='round',
            stroke_dasharray=None,
            perpendicular_offset=None,

            feature_label=False,
            font_family='Aerial',
            font_color="#333333",
            font_size=14,
            font_weight='normal',
            font_style="normal",
            halo_color="#ffffff",
            halo_radius=1,

            raster_min_value=0,
            raster_max_value=100,
            continuous_legend=True,
    ):

        Pg.__init__(self, dbname, user, password, host, port)

        ClassifiedStyle.__init__(
            self,
            attribute_name=attribute_name,
            values=values,
            color_palette=color_palette,
            number_of_class=number_of_class,
            classification_method=classification_method,
            style_name=style_name,
            geom_type=geom_type,
            fill_color=fill_color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            opacity=opacity,

            point_size=point_size,
            well_known_name=well_known_name,
            point_rotation=point_rotation,
            stroke_linecap=stroke_linecap,
            stroke_dasharray=stroke_dasharray,
            perpendicular_offset=perpendicular_offset,

            feature_label=feature_label,
            font_family=font_family,
            font_color=font_color,
            font_size=font_size,
            font_weight=font_weight,
            font_style=font_style,
            halo_color=halo_color,
            halo_radius=halo_radius
        )

        RasterStyle.__init__(
            self,
            style_name=style_name,
            color_palette=color_palette,
            number_of_class=number_of_class,
            min_value=raster_min_value,
            max_value=raster_max_value,
            opacity=opacity,
            continuous_legend=continuous_legend
        )

        # The schema of the table from postgresql
        self.schema = schema
        self.pg_table_name = pg_table_name

    def get_attribute_name(self):

        if self.attribute_name is None:
            if self.conn is None:
                self.connect()

            columns = self.get_column_names(self.pg_table_name)

            return random.choice(columns)

        else:
            return self.attribute_name

    def get_attribute_values(self):
        if self.conn is None:
            self.connect()

        self.values = self.get_values_from_column(
            column=self.attribute_name, table=self.pg_table_name, schema=self.schema)

        for i, v in enumerate(self.values):
            if type(v) is str:
                val = str_to_num(v)
                self.values[i] = val

        self.max_value = max(self.values)
        self.min_value = min(self.values)

    def generate_simple_style(self):
        return self.simple_style()

    def generate_catagorized_style(self):
        return self.catagorized_style()

    def generate_classified_style(self):
        return self.classified_style()

    def generate_raster_style(self):
        return self.coverage_style()
