import seaborn as sns
from matplotlib.colors import rgb2hex


class FeatureError:
    pass


class VectorColorPalette:
    '''
    The class will used to create the color palette objects
    The object will be used for point, line and polygon features
    '''

    def __init__(self, color_palette="Spectral_r", number_of_class=5):
        self.color_palette = color_palette
        self.number_of_class = number_of_class
        self.color_palette_selector()

    def color_palette_selector(self):
        if type(self.color_palette) is dict:
            self.number_of_class = len(self.color_palette)
            self.color_palette = list(self.color_palette.values())

        else:
            palette = sns.color_palette(
                self.color_palette, int(self.number_of_class))
            self.color_palette = [rgb2hex(i) for i in palette]


class RasterColorPalette:
    '''
    The object will be used for the raster styling
    '''

    def __init__(self, color_palette="Spectral_r", number_of_class=5):
        self.color_palette = color_palette
        self.number_of_class = number_of_class


def str_to_num(input_str):

    try:
        if '.' in input_str:
            val = float(input_str)
        else:
            val = int(input_str)
        return val

    except ValueError:
        pass
