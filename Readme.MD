[![Downloads](https://pepy.tech/badge/pysld)](https://pepy.tech/project/pysld) 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Pysld

The library is useful for generating the [SLD](https://www.ogc.org/standards/sld) file for raster as well as vector datasets. The package can generate the 4 types of styles,

1. Simple style
2. Categorized style
3. Classified style
4. Raster style

The library is the small version of [QGIS symbology](https://docs.qgis.org/2.8/en/docs/training_manual/basic_map/symbology.html). This library is very useful for the visual appearance on the map. Below is the example of categorized style in qgis. 

![categorized style qgis](https://github.com/iamtekson/pySLD/blob/main/docs/source/img/categorized_style_qgis.PNG?raw=true, "Categorized style in qgis")


The package is available in official PyPI: https://pypi.org/project/pysld/

The complete documentation of this library is found here: https://pysld.readthedocs.io

# Installation

```python
pip install pysld
```

# Some example

```python
# Import library
from pysld.style import StyleSld

# Simple style for polygon feature
simple_sld = StyleSld(style_name='polygonStyle', geom_type='polygon', fill_color='#ffffff', stroke_color='#333333')
simple_sld_style = simple_sld.generate_simple_style()
print(simple_sld_style)

# Categorized style for polygon feature
categorized_sld = StyleSld(
            style_name='polygonStyle',
            geom_type='polygon',
            attribute_name='USE',
            values=['Agriculture', 'Residential', 'Restaurant', 'Storehouse'],
            color_palette='Spectral_r')
categorized_sld_style = categorized_sld.generate_categorized_style()
print(categorized_sld_style)

# Classified style for polygon feature
classified_sld = StyleSld(
            style_name='polygonStyle',
            geom_type='polygon',
            attribute_name='USE',
            values=[1,2,3,34,23,122,12,2,3,21,23,32,1,23,42,1,23,1,1,23,4,3,54,6,768,8,554,3,43,543,6,657,7,75,4,4],
            number_of_class=5,
            classification_method='natural_break',
            color_palette='Spectral_r')
classified_sld_style = classified_sld.generate_classified_style()
print(classified_sld_style)

# Raster style
raster_style = StyleSld(style_name='polygonStyle',color_palette='Spectral_r',continuous_legend=True)
raster_sld_style = raster_sld.generate_raster_style(max_value=100, min_value=0)

# Categorized style for PostGIS data
categorized_sld = StyleSld(
            style_name='polygonStyle',
            geom_type='polygon',
            attribute_name='USE',
            color_palette='Spectral_r',
            # Postgres connection parameters
            dbname='postgres',
            user='postgres',
            password='admin',
            host='localhost',
            port='5432',
            schema='public',
            pg_table_name='postgres_table_name')
print(categorized.values) # It will print the unique values from postgres_table_name table
categorized_style_sld = categorized.generate_categorized_style()
```

### Generated SLD file example

##### Simple SLD

```xml
<StyledLayerDescriptor version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <NamedLayer>
        <Name>style</Name>
        <UserStyle>
        <Title>style</Title>
        <FeatureTypeStyle>
    <Rule>
        <PolygonSymbolizer>
            <Fill>
                <CssParameter name="fill">#ffffff</CssParameter>
                <CssParameter name="fill-opacity">1</CssParameter>
            </Fill>
            <Stroke>
                <CssParameter name="stroke">#333333</CssParameter>
                <CssParameter name="stroke-width">1</CssParameter>
            </Stroke>
        </PolygonSymbolizer>
    </Rule>
        </FeatureTypeStyle>
        </UserStyle>
    </NamedLayer>
</StyledLayerDescriptor>
```

##### Raster SLD

```xml
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" version="1.0.0" xmlns:ogc="http://www.opengis.net/ogc" xmlns:sld="http://www.opengis.net/sld">
    <UserLayer>
        <sld:LayerFeatureConstraints>
        <sld:FeatureTypeConstraint/>
        </sld:LayerFeatureConstraints>
        <sld:UserStyle>
        <sld:Name>polygonStyle</sld:Name>
        <sld:FeatureTypeStyle>
            <sld:Rule>
            <sld:RasterSymbolizer>
                <Opacity>1</Opacity>
                <sld:ChannelSelection>
                <sld:GrayChannel>
                    <sld:SourceChannelName>1</sld:SourceChannelName>
                </sld:GrayChannel>
                </sld:ChannelSelection>
                <sld:ColorMap type="range">
                    <sld:ColorMapEntry color="#54aead" label=" 0.0" quantity="0.0"/>
                    <sld:ColorMapEntry color="#bfe5a0" label=" 25.0" quantity="25.0"/>
                    <sld:ColorMapEntry color="#fffebe" label=" 50.0" quantity="50.0"/>
                    <sld:ColorMapEntry color="#fdbf6f" label=" 75.0" quantity="75.0"/>
                    <sld:ColorMapEntry color="#e95c47" label=" 100.0" quantity="100.0"/>
                </sld:ColorMap>
            </sld:RasterSymbolizer>
            </sld:Rule>
        </sld:FeatureTypeStyle>
        </sld:UserStyle>
    </UserLayer>
</StyledLayerDescriptor>
```
