import seaborn as sns
from matplotlib.colors import rgb2hex
from .support import RasterColorPalette


class RasterStyle(RasterColorPalette):
    def __init__(self, style_name='coverageStyle', color_palette='Spectral_r', number_of_class=5, opacity=1, continuous_legend=True, raster_cutoff_percentage=5):
        super().__init__(color_palette, number_of_class)
        self.style_name = style_name
        self.opacity = opacity
        self.continuous_legend = continuous_legend
        self.raster_cutoff_percentage = raster_cutoff_percentage

        # These fields are auto generated during style creation
        self.cmap_type = ''
        self.interval = None
        self.legend_label = []

    def legend_generator(self):
        self.interval = (self.max_value - self.min_value) / \
            (self.number_of_class - 1)

        if type(self.color_palette) is dict:
            self.legend_label = list(self.color_palette.keys())

        else:
            for i in range(len(self.color_palette)):
                val = self.min_value + self.interval * i
                self.legend_label.append(val)

    def color_palette_selector(self):
        if type(self.color_palette) is dict:
            self.number_of_class = len(self.color_palette)
            self.color_palette = list(self.color_palette.values())

        else:
            palette = sns.color_palette(
                self.color_palette, int(self.number_of_class))
            self.color_palette = [rgb2hex(i) for i in palette]

    def cmap_entry_generator(self):

        cmap_entry = ''
        for i, color, label in zip(range(self.number_of_class), self.color_palette, self.legend_label):
            val = self.min_value + self.interval * i

            if self.float_round:
                try:
                    label = round(label, self.float_round)

                except:
                    pass

            if (i == 0 and int(self.min_value) == 0):
                cmap_entry += '<sld:ColorMapEntry color="#000000" label=" 0" quantity="0" opacity="0"/>'

            else:
                cmap_entry += '<sld:ColorMapEntry color="{0}" label=" {1}" quantity="{2}"/> \n'.format(
                    color, label, val)

        return cmap_entry

    def coverage_style(self, max_value, min_value):

        self.max_value = max_value
        self.min_value = min_value

        if self.raster_cutoff_percentage:
            max_min_diff = self.max_value - self.min_value
            self.max_value = max_value - max_min_diff * self.raster_cutoff_percentage / 100
            self.min_value = min_value + max_min_diff * self.raster_cutoff_percentage / 100

        self.color_palette_selector()
        self.legend_generator()

        if self.continuous_legend:
            self.cmap_type = 'range'

        else:
            self.cmap_type = 'values'

        cmap_entry = self.cmap_entry_generator()
        style = """
        <StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" version="1.0.0" xmlns:ogc="http://www.opengis.net/ogc" xmlns:sld="http://www.opengis.net/sld">
        <UserLayer>
            <sld:LayerFeatureConstraints>
            <sld:FeatureTypeConstraint/>
            </sld:LayerFeatureConstraints>
            <sld:UserStyle>
            <sld:Name>{2}</sld:Name>
            <sld:FeatureTypeStyle>
                <sld:Rule>
                <sld:RasterSymbolizer>
                    <Opacity>{3}</Opacity>
                    <sld:ChannelSelection>
                    <sld:GrayChannel>
                        <sld:SourceChannelName>1</sld:SourceChannelName>
                    </sld:GrayChannel>
                    </sld:ChannelSelection>
                    <sld:ColorMap type="{0}" extended='true'>
                        {1}
                    </sld:ColorMap>
                </sld:RasterSymbolizer>
                </sld:Rule>
            </sld:FeatureTypeStyle>
            </sld:UserStyle>
        </UserLayer>
        </StyledLayerDescriptor>
        """.format(self.cmap_type, cmap_entry, self.style_name, self.opacity)

        return style
