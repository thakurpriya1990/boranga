from rest_framework import serializers

import json

from django.contrib.gis.geos import GEOSGeometry
import geojson
from shapely.geometry import shape, mapping

def wkb_to_geojson(wkb):
    from shapely.wkt import loads

    geos_geometry = GEOSGeometry(wkb)
    shapely_geometry = loads(geos_geometry.wkt)
    geo_json = mapping(shapely_geometry)
    geo_json["properties"] = {"srid": geos_geometry.srid}

    return geo_json


def features_json_to_geosgeometry(features, srid=4326):
    return [feature_json_to_geosgeometry(feature, srid) for feature in features]


def feature_json_to_geosgeometry(feature, srid = 4326):
    if isinstance(srid, str) and srid.isnumeric():
        srid = int(srid)
    geo_json = mapping(geojson.loads(json.dumps(feature)))
    geom_shape = shape(geo_json.get("geometry"))

    return GEOSGeometry(geom_shape.wkt, srid=4326)

def transform_json_geometry(json_geom, from_srid, to_srid):
    feature_json = {"type": "Feature", "geometry": json_geom}
    geom = feature_json_to_geosgeometry(feature_json, from_srid)
    geom.transform(to_srid)

    return geom.json


def spatially_process_geometry(json_geom, operation, parameters=[], unit=None):
    if operation == "buffer":
        res_json = buffer_json_geometry(json_geom, *parameters, unit)
    else:
        raise serializers.ValidationError(
            f"Spatial operation {operation} not supported"
        )

    return res_json


def buffer_json_geometry(json_geom, distance, unit):
    geoms = features_json_to_geosgeometry(json_geom["features"])

    if unit == "m":
        # TODO: aea transform
        albers_wa_string = 'proj4: +proj=aea +lat_1=-17.5 +lat_2=-31.5 +lat_0=0 +lon_0=121 +x_0=0 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs'
        raise serializers.ValidationError("Buffer operation does not support unit 'm'")
    elif unit == "deg":
        buffer_geoms = [geom.buffer(distance) for geom in geoms]
    else:
        raise serializers.ValidationError(
            f"Buffer operation requires unit parameter, got {unit}"
        )

    feature_collection = {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature", "geometry": json.loads(geom.json), "properties": {}}
            for geom in buffer_geoms
        ],
    }

    return json.dumps(feature_collection)