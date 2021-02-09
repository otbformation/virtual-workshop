"""
Some functions for Jupyter displaying
- quicklook creation
- map displaying (imshow, ipyleaflet)
"""

import os
import datetime

import numpy as np
import matplotlib.pyplot as plt

import rasterio
from rasterio.warp import transform_bounds
from rasterio.warp import transform

import folium

# ignore rasterio FurtureWarnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from ipyleaflet import Map, Rectangle, ImageOverlay, FullScreenControl, DrawControl, LayersControl, GeoJSON


def normalize(array, quantile=2):
    """
    normalizes bands into 0-255 scale
    :param array: numpy array to normalize
    :param quantile: quantile for ignoring outliers
    """
    array = np.nan_to_num(array)
    array_min, array_max = np.percentile(array, quantile), np.percentile(array, 100-quantile)
    normalized = 255*((array - array_min)/(array_max - array_min))
    normalized[normalized>255] = 255
    normalized[normalized<0] = 0
    return normalized.astype(np.uint8)


def imshow_RGBPIR(raster, colors=["Red", "Blue", "Green", "NIR"]):
    """
    show R,G,B, PIR image
    :param array: raster (rasterio image)
    :param colors: colors names list
    """
    print ("Quicklook by channel")
    multiband = []
    fig, ax = plt.subplots(1,len(colors)+1, figsize=(21,7))
    for nfig, color in enumerate(colors):
        band = raster.read(nfig+1, out_shape=(int(raster.height/16), int(raster.width/16)))
        band = normalize(band)

        if nfig < 3: multiband.append(band)

        try:          
            ax[nfig].imshow(band, cmap=color+'s')
        except ValueError:
            ax[nfig].imshow(band, cmap='Oranges')
    
        ax[nfig].set_title(color+' channel')

    ax[len(colors)].imshow(np.dstack(multiband))
    ax[len(colors)].set_title(colors[0]+colors[1]+colors[2])


def write_quicklook(raster, filename, downfactor=4):
    """
    write a JPG preview
    :param raster: raster (rasterio image)
    :param filename: path to the output preview
    :param downfactor: downsampling factor
    """
    profile = raster.profile

    # update size in profile
    newwidth = int(raster.width/downfactor)
    newheight = int(raster.height/downfactor)

    try:
        aff = raster.affine
        newaffine = rasterio.Affine(aff.a/downfactor, aff.b, aff.c,
                                    aff.d, aff.e/downfactor, aff.f)

        profile.update(dtype=rasterio.uint8, count=3, compress='lzw', driver='JPEG',
                       width=newwidth, height=newheight, transform=newaffine, affine=newaffine)

    # depend on rasterio version
    except AttributeError:
        aff = raster.transform
        newaffine = rasterio.Affine(aff.a/downfactor, aff.b, aff.c,
                                    aff.d, aff.e/downfactor, aff.f)

        profile.update(dtype=rasterio.uint8, count=3, compress='lzw', driver='JPEG',
                       width=newwidth, height=newheight, transform=newaffine)

    # write raster
    with rasterio.open(filename, 'w', **profile) as dst:
        for n in range(3):
            if raster.count == 1:
                band = raster.read(1, out_shape=(int(raster.height/downfactor), int(raster.width/downfactor)))
            else:
                band = raster.read(n+1, out_shape=(int(raster.height/downfactor), int(raster.width/downfactor)))
                
            band = normalize(band)
            dst.write(band, n+1)


def rasters_on_map(rasters_list, out_dir, overlay_names_list, geojson_data=None):
    """
    displays a raster on a ipyleaflet map
    :param rasters_list: rasters to display (rasterio image)
    :param out_dir: path to the output directory (preview writing)
    :param overlay_names_list: name of the overlays for the map
    """
    # - get bounding box
    raster = rasters_list[0]
    epsg4326 = {'init': 'EPSG:4326'}
    bounds = transform_bounds(raster.crs, epsg4326, *raster.bounds)
    center = [(bounds[0]+bounds[2])/2, (bounds[1]+bounds[3])/2]

    # - get centered map
    m = Map(center=(center[-1], center[0]), zoom=10)

    # - plot quicklook
    for raster, overlay_name in zip(rasters_list, overlay_names_list):
        bounds = transform_bounds(raster.crs, epsg4326, *raster.bounds)
        quicklook_url = os.path.join(out_dir, "PREVIEW_{}.JPG".format(datetime.datetime.now()))
        write_quicklook(raster, quicklook_url)
        quicklook = ImageOverlay(
            url=quicklook_url,
            bounds=((bounds[1], bounds[0]),(bounds[3], bounds[2])),
            name=overlay_name
        )
        m.add_layer(quicklook)
    m.add_control(LayersControl())
    m.add_control(FullScreenControl())

    # - add geojson data
    if geojson_data is not None:
        geo_json = GeoJSON(data=geojson_data,
                           style = {'color': 'green', 'opacity':1, 'weight':1.9, 'dashArray':'9', 'fillOpacity':0.1})
        m.add_layer(geo_json)
    
    # - add draw control
    dc = DrawControl()
    m.add_control(dc)

    return m, dc

def rasters_on_map_with_folium(rasters_list, out_dir, overlay_names_list, geojson_data=None):
    """
    displays a raster on a ipyleaflet map
    :param rasters_list: rasters to display (rasterio image)
    :param out_dir: path to the output directory (preview writing)
    :param overlay_names_list: name of the overlays for the map
    """
    # - get bounding box
    raster = rasters_list[0]
    epsg4326 = {'init': 'EPSG:4326'}
    bounds = transform_bounds(raster.crs, epsg4326, *raster.bounds)
    center = [(bounds[0]+bounds[2])/2, (bounds[1]+bounds[3])/2]

    # - get centered map
    m = folium.Map(location=(center[-1], center[0]),start_zoom=10)

    # - plot quicklook
    for raster, overlay_name in zip(rasters_list, overlay_names_list):
        bounds = transform_bounds(raster.crs, epsg4326, *raster.bounds)
        quicklook_url = os.path.join(out_dir, "PREVIEW_{}.JPG".format(datetime.datetime.now()))
        write_quicklook(raster, quicklook_url)
        quicklook = folium.raster_layers.ImageOverlay(
            quicklook_url,
            ((bounds[1], bounds[0]),(bounds[3], bounds[2])),
            name=overlay_name
        )
        m.add_children(quicklook)

    # - add geojson data
    if geojson_data is not None:
        geo_json = GeoJSON(data=geojson_data,
                           style = {'color': 'green', 'opacity':1, 'weight':1.9, 'dashArray':'9', 'fillOpacity':0.1})
        m.add_children(geo_json)

    return m




def get_bounding_box_from_draw(raster, dc):
    """
    returns bounding box in a image
    :param raster: displayed raster (rasterio image)
    :param dc: drawcontrol ipyleaflet
    """
    try:
        # Get last draw from the map
        coordinates = np.array(dc.last_draw['geometry']['coordinates'][0])

        # lon, lat to Sentinel-2 coordinate reference system
        lon_min_max = [np.amin(coordinates[:,0]), np.amax(coordinates[:,0])]
        lat_min_max = [np.amin(coordinates[:,1]), np.amax(coordinates[:,1])]
        lons, lats = np.meshgrid(lon_min_max, lat_min_max)
        xs, ys = transform({'init': 'EPSG:4326'}, raster.crs, lons.flatten(), lats.flatten())

        # Get the region of interest in the image
        rows, cols = [], []
        for x, y in zip(xs, ys):
            row, col = ~raster.affine * (x, y)
            rows.append(row)
            cols.append(col)
        row_min, row_max = np.amin(rows), np.amax(rows)
        col_min, col_max = np.amin(cols), np.amax(cols)
        startx, starty = map(lambda v:int(np.floor(v)), [col_min, row_min])
        endx, endy = map(lambda v:int(np.ceil(v)), [col_max, row_max])
        print ("Bounding box computed")
    except:
        print ("Draw a polygon in the displayed map")
        startx, starty, endx, endy = None, None, None, None
    return startx, starty, endx, endy
