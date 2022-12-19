import grass.script as gs
import urllib.request
import xml.etree.ElementTree as et
import os


# Constants
URL = 'https://geoserveis.icgc.cat/icc_mapesbase/wms/service?' 


# User defined parameters
layers = ['mtc2000m', 'mtc1000m', 'mtc500m', 'mtc250m', 'mtc100m', 'mtc50m']
output = 'C:\\IGCG\\'


def main():
    for layer in layers:
        if not os.path.exists(output):
           os.makedirs(output)

        # Get WMS capabilities
        capabilities = urllib.request.urlopen(URL + 'REQUEST=GetCapabilities').read()

        xml_root = et.fromstring(capabilities)

        # Find layer bounds and resolution
        xpath = './Capability/Layer/Layer[Name=\'' + layer + '\']/BoundingBox[@SRS=\'EPSG:4326\']'
        xml_bounding_box = xml_root.findall(xpath)[0]

        maxx = xml_bounding_box.get('maxx')
        maxy = xml_bounding_box.get('maxy')
        minx = xml_bounding_box.get('minx')
        miny = xml_bounding_box.get('miny')
        resx = xml_bounding_box.get('resx')

        gs.run_command('g.region', e=maxx, n=maxy, w=minx, s=miny, res=resx)

        # Query WMS
        # The default driver (WMS_GRASS) does not work. WMS_GDAL sometimes returns an error but saves the data.
        gs.run_command('r.in.wms', overwrite=True, url=URL, output=layer, layers=layer, format='tiff', driver='WMS_GDAL')

        # Fill nulls with black
        gs.run_command('r.null', map=layer, null=0)

        # Save data in 3 bands to increase software compatibility. TwoNav Land does not read correctly a single int16 band.
        layer_r = layer + '_r'
        layer_g = layer + '_g'
        layer_b = layer + '_b'
        gs.run_command('r.rgb', overwrite=True, input=layer, red=layer_r, green=layer_g, blue=layer_b)

        layer_rgb = layer + '_rgb'
        gs.run_command('i.group', group=layer_rgb, input=layer_r + ',' + layer_g + ',' + layer_b)

        layer_output = os.path.join(output, layer + '.tiff')
        gs.run_command('r.out.gdal', overwrite=True, input=layer_rgb, output=layer_output, type='Byte', createopt='PROFILE=GeoTIFF,INTERLEAVE=PIXEL')

        # Clean all temporal layers
        gs.run_command('g.remove', type='all', flags='f', name=layer)
        gs.run_command('g.remove', type='all', flags='f', name=layer_r)
        gs.run_command('g.remove', type='all', flags='f', name=layer_g)
        gs.run_command('g.remove', type='all', flags='f', name=layer_b)
        gs.run_command('g.remove', type='all', flags='f', name=layer_rgb)

        # Clean unwanted files
        layer_output_aux = os.path.join(output, layer + '.tiff.aux.xml')
        os.remove(layer_output_aux)


if __name__ == "__main__":
    main()