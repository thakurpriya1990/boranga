from rest_framework import serializers

import sys
import json

from django.contrib.gis.geos import GEOSGeometry
import geojson
from shapely.geometry import Point, MultiPoint, Polygon, MultiPolygon, shape, mapping
from shapely.ops import transform, unary_union, voronoi_diagram

import numpy as np

from itertools import combinations

# Albers Equal Area projection string for Western Australia
aea_wa_string = "+proj=aea +lat_1=-17.5 +lat_2=-31.5 +lat_0=0 +lon_0=121 +x_0=0 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"


def wkb_to_geojson(wkb):
    from shapely.wkt import loads

    geos_geometry = GEOSGeometry(wkb)
    shapely_geometry = loads(geos_geometry.wkt)
    geo_json = mapping(shapely_geometry)
    geo_json["properties"] = {"srid": geos_geometry.srid}

    return geo_json


def features_json_to_geosgeometry(features, srid=4326):
    return [feature_json_to_geosgeometry(feature, srid) for feature in features]


def feature_json_to_geosgeometry(feature, srid=4326):
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
    geoms = features_json_to_geosgeometry(json_geom["features"])

    try:
        # Function from string
        spatial_operation = getattr(sys.modules[__name__], operation)
    except AttributeError:
        raise serializers.ValidationError(
            f"Spatial operation {operation} not supported"
        )
    else:
        res_json = spatial_operation(geoms, *parameters, unit)

    return res_json


def feature_collection(geoms):
    return {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature", "geometry": json.loads(geom.json), "properties": {}}
            for geom in geoms
        ],
    }


def projection(crs_from, crs_to):
    from pyproj import Transformer

    transformer = Transformer.from_crs(
        crs_from,
        crs_to,
        always_xy=True,
    )
    return transformer.transform


def projection_4326_to_aea_wa():
    return projection(4326, aea_wa_string)


def projection_aea_wa_to_4326():
    return projection(aea_wa_string, 4326)


def polygon_points(polygon):
    return [Point(p) for p in polygon.exterior.coords]


def buffer_point_m(point, distance):
    pnt_buffered = transform(projection_4326_to_aea_wa(), point).buffer(distance)
    return transform(projection_aea_wa_to_4326(), pnt_buffered)


def buffer_polygon_m(polygon, distance):
    # Transform the polygon exterior points to AEA WA
    linear_ring = polygon.exterior_ring.coords
    pnts = [Point(p) for p in linear_ring]
    pnts_transformed = [transform(projection_4326_to_aea_wa(), p) for p in pnts]

    # Create a polygon from the the transformed points and buffer it
    plg_buffered = Polygon(pnts_transformed).buffer(distance)

    # Transform the buffered polygon's exterior points back to 4326
    xy = plg_buffered.exterior.coords.xy
    plg_buffered_pnts = [Point(p) for p in list(zip(xy[0], xy[1]))]

    return Polygon(
        [transform(projection_aea_wa_to_4326(), p) for p in plg_buffered_pnts]
    )


def buffer_geometries(geoms, distance, unit):
    if unit == "m":
        buffered_geoms = []
        for geom in geoms:

            if geom.dims == 0:
                # A point
                pnt = Point(geom)
                buffer_geom = buffer_point_m(pnt, distance)
            elif geom.dims == 1:
                raise serializers.ValidationError(
                    "Buffer operation not supported for LineString (dim-1)"
                )
            else:
                # A polygon (dim 2), can there possibly be a dim-3 geometry?
                buffer_geom = buffer_polygon_m(geom, distance)

            buffered_geoms.append(GEOSGeometry(buffer_geom.wkt))

    elif unit == "deg":
        buffered_geoms = [geom.buffer(distance) for geom in geoms]
    else:
        raise serializers.ValidationError(
            f"Buffer operation requires unit parameter, got {unit}"
        )

    return json.dumps(feature_collection(buffered_geoms))


def convex_hull(geoms, *args, **kwargs):
    convex_hull = MultiPoint(geoms).convex_hull
    geom = GEOSGeometry(convex_hull.wkt)

    return json.dumps(feature_collection([geom]))


def intersect_geometries(geoms, *args, **kwargs):
    """Calculates the intersection of the input geometries."""

    if len(geoms) < 2:
        raise serializers.ValidationError(
            "Intersection operation requires more than one geometry"
        )
    if not geoms[0].intersects(geoms[1]):
        raise serializers.ValidationError(
            "Intersection operation requires intersecting geometries"
        )

    intersection = unary_union(
        MultiPolygon([a.intersection(b) for a, b in combinations(geoms, 2)])
    )

    geom = GEOSGeometry(intersection.wkt)

    return json.dumps(feature_collection([geom]))


def union_geometries(geoms, *args, **kwargs):
    """Calculates the union of the input geometries."""

    mp = MultiPolygon(geoms)
    unary_union_geoms = unary_union(mp)
    union_geom = GEOSGeometry(unary_union_geoms.wkt)

    return json.dumps(feature_collection([union_geom]))


def voronoi(geoms, *args, **kwargs):
    """Calculates the Voronoi diagram of the input geometries."""

    mp = MultiPoint(geoms)
    voronoi = voronoi_diagram(mp)
    voronoi_geom = GEOSGeometry(MultiPolygon(voronoi).wkt)

    return json.dumps(feature_collection([voronoi_geom]))


def centroid(geoms, *args, **kwargs):
    """Calculates the centroid of the input geometries."""

    centroid = MultiPolygon(geoms).centroid
    geom = GEOSGeometry(centroid.wkt)

    return json.dumps(feature_collection([geom]))


def mean_center_point(geoms):
    # the mean of the input coordinates (see: https://shapely.readthedocs.io/en/stable/reference/shapely.centroid.html)
    return MultiPoint(geoms).centroid


def mean_center(geoms, *args, **kwargs):
    """Calculates the mean center point of the input geometries."""

    geom = GEOSGeometry(mean_center_point(geoms).wkt)

    return json.dumps(feature_collection([geom]))


def standard_distance(geoms, *args, **kwargs):
    """Calculates the standard distance deviation, the average distance all features
    vary from the mean center point of the input geometries.
    Returns a circle with the mean center point as center and the standard distance as radius,
    indicating the compactness of the input geometries.
    """

    mean = mean_center_point(geoms)
    n = len(geoms)

    X = [np.power(p.x - mean.x, 2) for p in geoms]
    Y = [np.power(p.y - mean.y, 2) for p in geoms]

    std = np.sqrt(np.sum(X) / n + np.sum(Y) / n)

    return buffer_geometries([GEOSGeometry(mean.wkt)], std, "deg")
