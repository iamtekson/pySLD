import random
from .postgres import Pg
from .classifiedStyle import ClassifiedStyle
from .rasterStyle import RasterStyle
from matplotlib.colors import rgb2hex
from .support import str_to_num


class StyleSld (ClassifiedStyle, RasterStyle,  Pg):
    """
    This is the main style class for generating the SLD files.

    There are mainly 4 types of styles based on the data
        1. SIMPLE : Valid for point, line, polygon features
        2. CATEGORIZED : Valid for point, line, polygon features
        3. CLASSIFIED : Valid for point, line, polygon features
        4. RASTER : Valid for raster dataset

    Simple Style:
    =============
    The simple style 


    Parameters:
    -----------
    attribute_name : str
        Required: For CLASSIFIED and CATEGORIZED style / Not required for SIMPLE and RASTER style
        Default Value: None
        Description: 

    values: array 
        Required: For CLASSIFIED and CATEGORIZED style / Not required for SIMPLE and RASTER style
        Default Value: None
        Description: 

    number_of_class : int 
        Required: For CLASSIFIED style / Not required for SIMPLE, CATEGORIZED and RASTER style
        Default Value: 5
        Description: The number of classes for the CATEGORIZED style is equal to length of `values`

    color_palette : str, list, dict 
        Required: For CATEGORIZED, CLASSIFIED AND RASTER style / Not required for SIMPLE style
        Default Value: 'Spectral_r'
        Description: 

    style_name : str 
        Required: Required
        Default Value: 'style'
        Description: 

    geom_type : str 
        Required: For CATEGORIZED, CLASSIFIED AND SIMPLE style / Not required for RASTER style
        Default Value: 'polygon'
        Available Values: 'point', 'line', 'polygon' 
        Description: 

    classification_method: str
        Required: For CLASSIFIED style / Not required for CATEGORIZED, RASTER AND SIMPLE style
        Default Value: 'natural_break'
        Available Values: 'natural_break', 'equal_interval', 'quantile', 'standard_deviation', 'geometrical_interval'

    fill_color: str, color_code
        Required: For SIMPLE style
        Default Value: '#ffffff'

    stroke_color: str, color_code
        Required: For SIMPLE, CATEGORIZED, AND CLASSIFIED style
        Default Value: '#333333'

    stroke_width: numeric
        Required: For SIMPLE, CATEGORIZED, AND CLASSIFIED style
        Default Value: 1


    opacity: numeric, value between 0 and 1
        Required: Required
        Default Value: 1

    dbname: str
        Required: Optional
        Default Value: None

    user: str

    password: str

    host: str

    schema: str

    pg_table_name: str

    point_size: int

    well_known_name: str

    point_roration: int

    stroke_linecap: str

    stroke_dasharray: str

    perpendicular_offset: str

    feature_label: bool

    font_family: str

    font_color: str, color_code

    font_size: int

    font_weight: str

    font_style: str

    halo_color: str, color_code

    halo_radius: numeric

    continuous_legend: bool

    float_round: int, It will help to round the element, see more in classification.round_values
    """

    def __init__(
            self,
            attribute_name=None,
            values=None,
            number_of_class=5,
            float_round=2,
            color_palette="Spectral_r",
            style_name='style',
            geom_type='polygon',
            classification_method='natural_break',
            fill_color='#ffffff',
            stroke_color="#333333",
            stroke_width=1,
            stroke_opacity=1,
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
            continuous_legend=True,
            raster_cutoff_percentage=None,
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
            stroke_opacity=stroke_opacity,
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
            opacity=opacity,
            continuous_legend=continuous_legend,
            raster_cutoff_percentage=raster_cutoff_percentage,
        )

        # The schema of the table from postgresql
        self.schema = schema
        self.pg_table_name = pg_table_name

        # Other settings
        self.float_round = float_round

    def connect_pg(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        # self.connect()
        # self.connect_db()

    def get_attribute_name(self, pg_table_name=None):
        '''
        Help to connect with postgresql and set the attribute_name.
        The attribute name will be the column_name of the shapefile attribute table.
        '''

        # if self.conn is None:
            # self.connect()
            # self.connect_db()

        if pg_table_name is not None:
            self.pg_table_name = pg_table_name

        if self.attribute_name is None:
            # Function to get the column_names from postgres
            columns = self.get_column_names(self.pg_table_name)

            self.attribute_name = random.choice(columns)

            return self.attribute_name

        else:
            return self.attribute_name

    def get_values_from_pg(self, sql_query=None):
        """
        Get the values from postgresql and set it to self.values


        Parameters used:
        ----------------
        self.conn : connection class
            It will be automatically connected if user provides the connection parameters

        self.values : array
            The values from specific column of postgres

        self.attribute_name: str
            The column name of the table

        self.pg_table_name: str

        self.schema: str
        """
        # if self.conn is None:
            # self.connect()
            # self.connect_db()

        if self.attribute_name is None:
            self.attribute_name = self.get_attribute_name()

        if sql_query is not None:
            self.values = self.get_values_from_sql(sql_query)

        else:
            self.values = self.get_values_from_column(
                column=self.attribute_name, table=self.pg_table_name, schema=self.schema)

        return self.values

    def generate_simple_style(self):
        return self.simple_style()

    def generate_categorized_style(self, values=None):

        if values:
            self.values = values

        if self.values is None:
            self.get_values_from_pg()

        self.number_of_class = len(self.values)

        return self.categorized_style()

    def generate_classified_style(self, values=None):
        if values:
            self.values = values

        if self.values is None:
            self.get_values_from_pg()

        return self.classified_style()

    def generate_raster_style(self, max_value, min_value):
        return self.coverage_style(max_value, min_value)
