from .support import FeatureError


class FeatureLabel:
    def __init__(self, attribute_name_label=None, geom_type='polygon', font_family='Aerial', font_color="#333333", font_size=14, font_weight='normal', font_style="normal", halo_color="#ffffff", halo_radius=1):
        self.attribute_name_label = attribute_name_label
        self.geom_type = geom_type
        self.font_family = font_family
        self.font_color = font_color
        self.font_size = font_size
        self.font_weight = font_weight
        self.font_style = font_style
        self.halo_color = halo_color
        self.halo_radius = halo_radius

        # for point style
        self.offset_x = 0
        self.offset_y = 0
        self.displacement_x = 0
        self.displacement_y = 0
        self.rotation = 0

        # for line style
        self.perpendicular_offset = 0

    def generate_point_or_polygon_label(self):
        '''
        All the values are in pixel
        '''

        if self.attribute_name_label is None:
            _label = '<Label>Label</Label>'

        else:
            _label = '<Label><ogc:PropertyName>{0}</ogc:PropertyName></Label>'

        label = '''
            <TextSymbolizer>
                {0}
                <Font>
                    <CssParameter name="font-family">{1}</CssParameter>
                    <CssParameter name="font-color">{2}</CssParameter>
                    <CssParameter name="font-size">{3}</CssParameter>
                    <CssParameter name="font-style">{4}</CssParameter>
                    <CssParameter name="font-weight">{5}</CssParameter>
                </Font>
                <LabelPlacement>
                    <PointPlacement>
                        <AnchorPoint>
                            <AnchorPointX>{6}</AnchorPointX>
                            <AnchorPointY>{7}</AnchorPointY>
                        </AnchorPoint>
                        <Displacement>
                            <DisplacementX>{8}</DisplacementX>
                            <DisplacementY>{9}</DisplacementY>
                        </Displacement>
                        <Rotation>{10}</Rotation>
                    </PointPlacement>
                </LabelPlacement>
                <Halo>
                    <Radius>{11}</Radius>
                    <Fill>
                        <CssParameter name="fill">{12}</CssParameter>
                    </Fill>
                </Halo>
            </TextSymbolizer>
            '''.format(_label, self.font_family, self.font_color,
                       self.font_size, self.font_style, self.font_weight,
                       self.offset_x, self.offset_y, self.displacement_x, self.displacement_y,
                       self.rotation, self.halo_radius, self.halo_color)

        return label

    def generate_line_label(self):
        if self.attribute_name_label is None:
            _label = '<Label>Label</Label>'

        else:
            _label = '<Label><ogc:PropertyName>{0}</ogc:PropertyName></Label>'

        label = '''
            <TextSymbolizer>
                {0}
                <Font>
                    <CssParameter name="font-family">{1}</CssParameter>
                    <CssParameter name="font-color">{2}</CssParameter>
                    <CssParameter name="font-size">{3}</CssParameter>
                    <CssParameter name="font-style">{4}<CssParameter>
                    <CssParameter name="font-weight">{5}</CssParameter>
                </Font>
                <LabelPlacement>
                    <LinePlacement>
                        <PerpendicularOffset>{6}</PerpendicularOffset>
                    </LinePlacement>
                </LabelPlacement>
                <Halo>
                    <Radius>{7}</Radius>
                    <Fill>
                        <CssParameter name="fill">{8}</CssParameter>
                    </Fill>
                </Halo>
            </TextSymbolizer>
            '''.format(_label, self.font_family, self.font_color,
                       self.font_size, self.font_style, self.font_weight,
                       self.perpendicular_offset, self.halo_radius, self.halo_color)

        return label

    def generate_feature_label(self):
        geom_types = ['point', 'line', 'polygon']

        if self.geom_type == 'point':
            return self.generate_point_or_polygon_label()

        elif self.geom_type == 'line':
            return self.generate_line_label()

        elif self.geom_type == 'polygon':
            return self.generate_point_or_polygon_label()

        else:
            raise FeatureError('geom_type did not matched. Available geom_types are {}'.format(
                ', '.join(geom_types)))
