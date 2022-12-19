# IGCG Maps for TwoNav Devices

Here is a small gide on how I download and installed the latest maps from *Institut Cartogràfic de Catalunya* to a *TwoNav Aventura 2 device*.

Since *ICGC* does not provide a way to fully download a map, I extracted extracted the data using their own WMS.

## Get the layers from ICGC
1. Download [Grass Gis](https://grass.osgeo.org/).
2. *(Optional)* Modify the source code. Only required for some layers like `orto25m`:
    1. Locate `wms_gdal_dr.py` (e.g., `C:\Program Files\GRASS GIS 8.2\etc\r.in.wms`)
    2. Add the following code inside the `_createXML(self)` function:
        ```
        ZeroBlockHttpCodes = etree.SubElement(gdal_wms, "ZeroBlockHttpCodes")
        ZeroBlockHttpCodes.text = str(500)z
        ```
        It will look something like:
        ```
        ...
            
        if self.params["username"] and self.params["password"]:
            user_password = etree.SubElement(gdal_wms, "UserPwd")
            user_password.text = "%s:%s" % (
                self.params["username"],
                self.params["password"],
            )
    
        # BEGIN ADD CODE
        ZeroBlockHttpCodes = etree.SubElement(gdal_wms, "ZeroBlockHttpCodes")
        ZeroBlockHttpCodes.text = str(500)
        # END ADD CODE
    
        xml_file = self._tempfile()
    
        ...
        ```
3. Download and save this [Python script](./icgc_get_layers.py).
4. Open the script and mofiy `# User defined parameters`:
    1. Specify which layers do you want from the [available layers](https://geoserveis.icgc.cat/icc_mapesbase/wms/service?REQUEST=GetCapabilities).
    2. Set the output path.
5. Launch Grass Gis and on the GUI, and launch the edited script `File -> Launch script`.
5. Everything downloaded! You now have all layers downloaded in `GeoTiff` format.

## Convert the layers to TwoNav format
1. Download and install *TwoNav Land* (tested on *9.3*).
2. Open a downloaded  `.tiff` layer using `File -> Open file...`.
3. On the opened map `Right click -> File -> Save Map as...` save as type `CompeGPS RASTER maps (*.rmap, *rtmap)`.
4. Do the previous steps for all downloaded layers.
5. *(Optional)* Create a hypermap:
    1. Right click `Maps`, `New hypermap`
    2. Drag and drop all `.rmap` layers inside the hypermap.
    3. For each hypermap layer `Right Click -> Properties` and modify the `Near zoom` and `Far zoom`. For example use the following configuration:
        
        |             | Near Zoom (m/pixel) | Far Zoom (m/pixel) |
        |-------------|---------------------|--------------------|
        |**mtc1000m** | 200                 | Always Visible     |
        |**mtc2000m** | 100                 | 200                |
        |**mtc500m**  | 200                 | 50                 |
        |**mtc250**   | 50                  | 25                 |
        |**mtc100**   | 25                  | 10                 |
        |**mtc50**    | Always Visible      | 5                  |
        
        Sometimes Land gets bugged and does not allow to edit the layer properties. The hyerpmap can be easly edited witht a text editor since it is a simple xml.
6. Using *Land*, send all the layers and the hypermap to your device.