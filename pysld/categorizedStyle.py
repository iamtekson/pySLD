import seaborn as sns
from matplotlib.colors import rgb2hex
from .simpleStyle import SimpleStyle
from .support import VectorColorPalette


class categorizedStyle(SimpleStyle, VectorColorPalette):
    def __init__(self,
                 attribute_name,
                 values,
                 color_palette="Spectral_r",
                 style_name='style',
                 geom_type='polygon',
                 number_of_class=None,
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
                 halo_radius=1):

        SimpleStyle.__init__(self,
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

        self.attribute_name = attribute_name
        self.values = values

        self.number_of_class = number_of_class

        if self.number_of_class is None:
            number_of_class = len(values)

        VectorColorPalette.__init__(self, color_palette, number_of_class)

    def get_number_of_class(self):
        if self.values is None:
            raise ValueError('The values should be list of catagory')

        if self.number_of_class is None:
            self.number_of_class = len(self.values)

        # else:
        #     raise ValueError(
        #         'There is a problem during get_number_of_class method.')

    def point_symbolizer_generator(self, fill_color):
        symbolizer = '''
            <PointSymbolizer>
                <Graphic>
                    <Mark>
                        <WellKnownName>{0}</WellKnownName>
                        <Fill>
                            <CssParameter name="fill">{1}</CssParameter>
                            <CssParameter name="fill-opacity">{2}</CssParameter>
                        </Fill>
                        <Stroke>
                            <CssParameter name="stroke">{3}</CssParameter>
                            <CssParameter name="stroke-width">{4}</CssParameter>
                            <CssParameter name="stroke-opacity">{7}</CssParameter>
                        </Stroke>
                    </Mark>
                <Size>{5}</Size>
                <Rotation>{6}</Rotation>
                </Graphic>
            </PointSymbolizer>
        '''.format(self.well_known_name, fill_color, self.opacity, self.stroke_color, self.stroke_width, self.point_size, self.point_rotation, self.stroke_opacity)

        return symbolizer

    def line_symbolizer_generator(self, stroke_color):
        dasharray = ''
        perpendicular_offset = ''

        if self.stroke_dasharray:
            dasharray = '<CssParameter name="stroke-dasharray">{}</CssParameter>'.format(
                self.stroke_dasharray)

        if self.perpendicular_offset:
            perpendicular_offset = '<PerpendicularOffset>{}</PerpendicularOffset>'.format(
                self.perpendicular_offset)
        symbolizer = '''
                <LineSymbolizer>
                    <Stroke>
                        <CssParameter name="stroke">{0}</CssParameter>
                        <CssParameter name="stroke-width">{1}</CssParameter>
                        <CssParameter name="stroke-linecap">{2}</CssParameter> 
                        <CssParameter name="stroke-opacity">{5}</CssParameter>
                        {3}
                    </Stroke>
                    {4}
                </LineSymbolizer>
        '''.format(stroke_color, self.stroke_width, self.stroke_linecap, dasharray, perpendicular_offset, self.stroke_opacity)

        return symbolizer

    def polygon_symbolizer_generator(self, fill_color):
        symbolizer = '''
            <PolygonSymbolizer>
                    <Fill>
                        <CssParameter name="fill">{0}</CssParameter>
                        <CssParameter name="fill-opacity">{1}</CssParameter>
                    </Fill>
                    <Stroke>
                        <CssParameter name="stroke">{2}</CssParameter>
                        <CssParameter name="stroke-width">{3}</CssParameter>
                        <CssParameter name="stroke-opacity">{4}</CssParameter>
                    </Stroke>
                </PolygonSymbolizer>
        '''.format(fill_color, self.opacity, self.stroke_color, self.stroke_width, self.stroke_opacity)

        return symbolizer

    def categorized_rule_generator(self, attribute_value, fill_color):

        if self.geom_type == 'point':
            symbolizer = self.point_symbolizer_generator(fill_color)

        elif self.geom_type == 'line':
            symbolizer = self.line_symbolizer_generator(
                stroke_color=fill_color)

        elif self.geom_type == 'polygon':
            symbolizer = self.polygon_symbolizer_generator(fill_color)

        rule = '''
        <Rule>
            <Name>{0}</Name>
            <Title>{0}</Title>
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>{1}</ogc:PropertyName>
                    <ogc:Literal>{0}</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
            {2}
        </Rule>
        '''.format(attribute_value, self.attribute_name, symbolizer)

        return rule

    def categorized_style(self):

        self.get_number_of_class()
        self.color_palette_selector()

        rule = ''
        for val, color in zip(self.values, self.color_palette):
            rule += self.categorized_rule_generator(val, fill_color=color)

        return self.style_generator(rule)
