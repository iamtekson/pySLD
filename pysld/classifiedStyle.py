import seaborn as sns
from matplotlib.colors import rgb2hex
from .simpleStyle import SimpleStyle
from .support import VectorColorPalette
from .categorizedStyle import categorizedStyle
from .classification import Classification
from .featureLabel import FeatureLabel


class ClassifiedStyle(Classification, categorizedStyle, FeatureLabel):
    def __init__(self,
                 attribute_name,
                 values,
                 number_of_class=5,
                 color_palette="Spectral_r",
                 style_name='style',
                 geom_type='polygon',
                 classification_method='natural_break',
                 fill_color='#ffffff',
                 stroke_color="#333333",
                 stroke_width=1,
                 stroke_opacity=1,
                 opacity=1,

                 point_size=6,
                 well_known_name='circle',
                 point_rotation=0,
                 stroke_linecap='round',
                 stroke_dasharray=None,
                 perpendicular_offset=None,

                 feature_label=False,
                 attribute_name_label=None,
                 font_family='Aerial',
                 font_color="#333333",
                 font_size=14,
                 font_weight='normal',
                 font_style="normal",
                 halo_color="#ffffff",
                 halo_radius=1
                 ):

        categorizedStyle.__init__(
            self,
            attribute_name=attribute_name,
            values=values,
            color_palette=color_palette,
            number_of_class=number_of_class,
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
            attribute_name_label=attribute_name_label,
            font_family=font_family,
            font_color=font_color,
            font_size=font_size,
            font_weight=font_weight,
            font_style=font_style,
            halo_color=halo_color,
            halo_radius=halo_radius
        )

        Classification.__init__(
            self, values, number_of_class, classification_method)

    def classified_rule_generator(self, lower_limit, heigher_limit, color):
        if self.geom_type == 'point':
            symbolizer = self.point_symbolizer_generator(color)

        elif self.geom_type == 'line':
            symbolizer = self.line_symbolizer_generator(
                stroke_color=color)

        elif self.geom_type == 'polygon':
            symbolizer = self.polygon_symbolizer_generator(color)

        rule = '''
        <Rule>
            <Name> {0}-{1}</Name>
            <Title>{0}-{1}</Title>
            <ogc:Filter>
                    <ogc:And>
                    <ogc:PropertyIsGreaterThanOrEqualTo>
                        <ogc:PropertyName>{2}</ogc:PropertyName>
                        <ogc:Literal>{0}</ogc:Literal>
                    </ogc:PropertyIsGreaterThanOrEqualTo>
                    <ogc:PropertyIsLessThan>
                        <ogc:PropertyName>{2}</ogc:PropertyName>
                        <ogc:Literal>{1}</ogc:Literal>
                    </ogc:PropertyIsLessThan>
                    </ogc:And>
                </ogc:Filter>
            {3}
        </Rule>
        '''.format(lower_limit, heigher_limit, self.attribute_name, symbolizer)
        return rule

    def round_values(self, in_array, float_round):
        return [round(elem, float_round) for elem in in_array]

    def classified_style(self):

        rule = ''

        self.choose_classification_method()
        self.color_palette_selector()

        if self.float_round:
            self.classes = self.round_values(self.classes, self.float_round)

        if self.classes:
            for value, color, i in zip(self.classes, self.color_palette, range(self.number_of_class)):

                try:
                    lower_limit = self.classes[i]
                    heigher_limit = self.classes[i + 1]

                    # In last set of rule, need to increase the value by 0.1 so that it will be visualize in system. #5
                    if i == self.number_of_class - 1:
                        heigher_limit = round(self.classes[i+1] + 0.1, 2)

                    rule += self.classified_rule_generator(
                        lower_limit, heigher_limit, color)

                except IndexError:
                    pass

            return self.style_generator(rule)

        else:
            raise ValueError(
                'The values column must be a list of numeric values.')
