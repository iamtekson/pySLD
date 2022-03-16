from .featureLabel import FeatureLabel
from .support import FeatureError


class SimpleStyle(FeatureLabel):
    def __init__(
            self,
            style_name='style',
            geom_type='polygon',
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

            attribute_name_label=None,
            feature_label=False,
            font_family='Aerial',
            font_color="#333333",
            font_size=14,
            font_weight='normal',
            font_style="normal",
            halo_color="#ffffff",
            halo_radius=1
    ):

        FeatureLabel.__init__(self, attribute_name_label, geom_type, font_family, font_color,
                              font_size, font_weight, font_style, halo_color, halo_radius)

        # Common properties
        self.style_name = style_name
        self.geom_type = geom_type
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.stroke_opacity = stroke_opacity,
        self.opacity = opacity
        self.feature_label = feature_label

        # For point
        self.point_size = point_size
        self.well_known_name = well_known_name
        self.point_rotation = point_rotation

        # For line
        self.stroke_linecap = stroke_linecap
        self.stroke_dasharray = stroke_dasharray
        self.perpendicular_offset = perpendicular_offset

    # This function is only for the support
    def style_generator(self, rule):

        if self.feature_label:
            label = self.generate_feature_label()
            label_rule = '''
                <Rule>
                    <Name/>
                    {}
                </Rule>
            '''.format(label)

        else:
            label_rule = ''

        style = '''
            <StyledLayerDescriptor version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <NamedLayer>
                    <Name>{0}</Name>
                    <UserStyle>
                    <Title>{0}</Title>
                    <FeatureTypeStyle>
                            {1}
                            {2}
                    </FeatureTypeStyle>
                    </UserStyle>
                </NamedLayer>
            </StyledLayerDescriptor>
        '''.format(self.style_name, rule, label_rule)

        return style

    def simple_point_style(self):
        point_rule = '''
            <Rule>
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
                        </Stroke>
                    </Mark>
                    <Size>{5}</Size>
                    <Rotation>{6}</Rotation>
                    </Graphic>
                </PointSymbolizer>
            </Rule>
        '''.format(self.well_known_name, self.fill_color, self.opacity, self.stroke_color, self.stroke_width, self.point_size, self.point_rotation)

        return self.style_generator(point_rule)

    def simple_line_style(self):
        dasharray = ''
        perpendicular_offset = ''

        if self.stroke_dasharray:
            dasharray = '<CssParameter name="stroke-dasharray">{}</CssParameter>'.format(
                self.stroke_dasharray)

        if self.perpendicular_offset:
            perpendicular_offset = '<PerpendicularOffset>{}</PerpendicularOffset>'.format(
                self.perpendicular_offset)
        line_rule = '''
            <Rule>
                <LineSymbolizer>
                    <Stroke>
                        <CssParameter name="stroke">{0}</CssParameter>
                        <CssParameter name="stroke-width">{1}</CssParameter>
                        <CssParameter name="stroke-linecap">{2}</CssParameter> 
                        {3}
                    </Stroke>
                    {4}
                </LineSymbolizer>
            </Rule>
        '''.format(self.stroke_color, self.stroke_width, self.stroke_linecap, dasharray, perpendicular_offset)

        return self.style_generator(line_rule)

    def simple_polygon_style(self):
        polygon_rule = '''
                <Rule>
                    <PolygonSymbolizer>
                        <Fill>
                            <CssParameter name="fill">{0}</CssParameter>
                            <CssParameter name="fill-opacity">{1}</CssParameter>
                        </Fill>
                        <Stroke>
                            <CssParameter name="stroke">{2}</CssParameter>
                            <CssParameter name="stroke-width">{3}</CssParameter>
                        </Stroke>
                    </PolygonSymbolizer>
                </Rule>
                '''.format(self.fill_color, self.opacity, self.stroke_color, self.stroke_width)

        return self.style_generator(polygon_rule)

    def simple_style(self):
        geom_types = ['point', 'line', 'polygon']

        if self.geom_type == 'point':
            return self.simple_point_style()

        elif self.geom_type == 'line':
            return self.simple_line_style()

        elif self.geom_type == 'polygon':
            return self.simple_polygon_style()

        elif self.geom_type == 'raster':
            pass

        else:
            raise FeatureError('geom_type did not matched. Available geom_types are {}'.format(
                ', '.join(geom_types)))
