import logging
import re

from django.apps import apps
from django.db.models import Q
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt

from boranga import settings
from boranga.components.spatial.models import Proxy, TileLayer
from boranga.helpers import is_internal

from rest_framework import serializers

import sys
import json
import geojson

from django.contrib.gis.geos import GEOSGeometry, Polygon

# from shapely.geometry import Point, MultiPoint, Polygon, MultiPolygon, shape, mapping
import shapely.geometry as shp
from shapely import wkt
from shapely.ops import transform, unary_union, voronoi_diagram

import numpy as np

from itertools import combinations

import requests

logger = logging.getLogger(__name__)

# Albers Equal Area projection string for Western Australia
aea_wa_string = "+proj=aea +lat_1=-17.5 +lat_2=-31.5 +lat_0=0 +lon_0=121 +x_0=0 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"


def invert_xy_coordinates(geometries):
    geometries = [transform(lambda x, y: (y, x), wkt.loads(p.wkt)) for p in geometries]
    geometries = [GEOSGeometry.from_ewkt(p.wkt) for p in geometries]

    return geometries


def intersect_geometry_with_layer(geometry, intersect_layer):
    geoserver_url = intersect_layer.geoserver_url
    intersect_layer_name = intersect_layer.layer_name
    invert_xy = intersect_layer.invert_xy

    if invert_xy:
        test_geom = invert_xy_coordinates([geometry])[0]

    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeName": f"{intersect_layer_name}",
        "maxFeatures": "5000",
        "srsName": "EPSG:4326",  # using the default projection for open layers and geodjango
        "outputFormat": "application/json",
        "propertyName": "SHAPE",
        "CQL_FILTER": f"INTERSECTS(SHAPE, {test_geom.wkt})",
    }

    request_path = (
        re.match(r"^\/geoproxy\/(?P<request_path>[\w-]+)/.*$", geoserver_url.url)
        .groupdict()
        .get("request_path", None)
    )
    if request_path:
        proxy = Proxy.objects.get(request_path=request_path)
        url = proxy.proxy_url
        auth_name = proxy.username
        auth_password = proxy.password
        res = requests.post(url + "wfs", params=params, auth=(auth_name, auth_password))
    else:
        res = requests.post(geoserver_url.url, params=params)

    return res.json()


def save_geometry(
    request,
    instance,
    geometry_data,
    instance_fk_field_name=None,
    component="occurrence",
    app_label="boranga",
):
    """
    Save geometry data to the database for an instance of a model.
    Args:
        request: The request object
        instance: The instance of the model to save the geometry for
        geometry_data: The geometry data to save
        instance_fk_field_name: The name of the foreign key field on the geometry model
        component: The component name
        app_label: The app label
    """

    instance_model_name = instance._meta.model.__name__

    if not geometry_data:
        logger.warn(f"No {instance_model_name} geometry to save")
        return

    InstanceGeometry = apps.get_model(
        app_label=app_label, model_name=f"{instance_model_name}Geometry"
    )
    InstanceGeometrySaveSerializer = getattr(
        sys.modules[f"boranga.components.{component}.serializers"],
        f"{instance_model_name}GeometrySaveSerializer",
    )
    if instance_fk_field_name is None:
        instance_fk_field_name = instance_model_name.lower()

    geometry = json.loads(geometry_data)
    if (
        0 == len(geometry["features"])
        and 0
        == InstanceGeometry.objects.filter(**{instance_fk_field_name: instance}).count()
    ):
        # No feature to save and no feature to delete
        logger.warn(f"{instance_model_name} geometry has no features to save or delete")
        return

    action = request.data.get("action", None)

    geometry_ids = []
    for feature in geometry.get("features"):
        supported_geometry_types = ["MultiPolygon", "Polygon", "MultiPoint", "Point"]
        geometry_type = feature.get("geometry").get("type")
        # Check if feature is of a supported type, continue if not
        if geometry_type not in supported_geometry_types:
            logger.warn(
                f"{instance_model_name}: {instance} contains a feature that is not a "
                f"{' or '.join(supported_geometry_types)}: {feature}"
            )
            continue

        logger.info(
            f"Processing {instance_model_name} {instance} geometry feature type: {geometry_type}"
        )

        geom_4326 = feature_json_to_geosgeometry(feature)

        original_geometry = feature.get("properties", {}).get("original_geometry")
        srid_original = original_geometry.get("properties", {}).get("srid", 4326)
        if not srid_original:
            raise ValidationError(
                f"Geometry must have an SRID set: {original_geometry.get('coordinates', [])}"
            )

        if not original_geometry.get("type", None):
            original_geometry["type"] = geometry_type
        feature_json = {"type": "Feature", "geometry": original_geometry}
        geom_original = feature_json_to_geosgeometry(feature_json, srid_original)

        geoms = [(geom_4326, geom_original)]

        for geom in geoms:
            geometry_data = {
                f"{instance_fk_field_name}_id": instance.id,
                "geometry": geom[0],
                "original_geometry_ewkb": geom[1].ewkb,
            }

            # TODO: Hardcoded. Possibly pass in via fn parameter whether to intersect and with what
            if instance_fk_field_name == "occurrence":
                intersect_layer = TileLayer.objects.get(
                    is_tenure_intersects_query_layer=True
                )
                data = intersect_geometry_with_layer(geom[0], intersect_layer)
                totalFeatures = data.get("totalFeatures")
                logger.info(
                    f"Geometry {geom[0]} intersects with {totalFeatures} features from {intersect_layer.layer_name}"
                )

                geometry_data["intersects"] = totalFeatures > 0
            else:
                logger.info("No intersect layer specified")

            if feature.get("id"):
                logger.info(
                    f"Updating existing {instance_model_name} geometry: {feature.get('id')} for: {instance}"
                )
                try:
                    geometry = InstanceGeometry.objects.get(id=feature.get("id"))
                except InstanceGeometry.DoesNotExist:
                    logger.warn(
                        f"{instance_model_name} geometry does not exist: {feature.get('id')}"
                    )
                    continue
                geometry_data["drawn_by"] = geometry.drawn_by
                geometry_data["locked"] = (
                    action in ["submit"]
                    and geometry.drawn_by == request.user.id
                    or geometry.locked
                )
                serializer = InstanceGeometrySaveSerializer(
                    geometry, data=geometry_data
                )
            else:
                logger.info(
                    f"Creating new geometry for {instance_model_name}: {instance}"
                )
                geometry_data["drawn_by"] = request.user.id
                geometry_data["locked"] = action in ["submit"]
                serializer = InstanceGeometrySaveSerializer(data=geometry_data)

            serializer.is_valid(raise_exception=True)
            geometry_instance = serializer.save()
            logger.info(f"Saved {instance_model_name} geometry: {geometry_instance}")
            geometry_ids.append(geometry_instance.id)

    # Remove any ocr geometries from the db that are no longer in the ocr_geometry that was submitted
    # Prevent deletion of polygons that are locked after status change (e.g. after submit)
    # or have been drawn by another user
    deleted_geometries = (
        InstanceGeometry.objects.filter(**{instance_fk_field_name: instance})
        .exclude(Q(id__in=geometry_ids) | Q(locked=True) | ~Q(drawn_by=request.user.id))
        .delete()
    )
    if deleted_geometries[0] > 0:
        logger.info(
            f"Deleted {instance_model_name} geometries: {deleted_geometries} for {instance}"
        )


def wkb_to_geojson(wkb):
    from shapely.wkt import loads

    geos_geometry = GEOSGeometry(wkb)
    shapely_geometry = loads(geos_geometry.wkt)
    geo_json = shp.mapping(shapely_geometry)
    geo_json["properties"] = {"srid": geos_geometry.srid}

    return geo_json


def features_json_to_geosgeometry(features, srid=4326):
    return [feature_json_to_geosgeometry(feature, srid) for feature in features]


def feature_json_to_geosgeometry(feature, srid=4326):
    if isinstance(srid, str) and srid.isnumeric():
        srid = int(srid)
    if "geometry" in feature:
        geo_json = feature
    else:
        # Convert feature to geojson
        geo_json = shp.mapping(geojson.loads(json.dumps(feature)))
    geom_shape = shp.shape(geo_json.get("geometry"))

    return GEOSGeometry(geom_shape.wkt, srid=srid)


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
    return [shp.Point(p) for p in polygon.exterior.coords]


def buffer_point_m(point, distance):
    pnt_buffered = transform(projection_4326_to_aea_wa(), point).buffer(distance)
    return transform(projection_aea_wa_to_4326(), pnt_buffered)


def buffer_polygon_m(polygon, distance):
    # Transform the polygon exterior points to AEA WA
    linear_ring = polygon.exterior_ring.coords
    pnts = [shp.Point(p) for p in linear_ring]
    pnts_transformed = [transform(projection_4326_to_aea_wa(), p) for p in pnts]

    # Create a polygon from the the transformed points and buffer it
    plg_buffered = shp.Polygon(pnts_transformed).buffer(distance)

    # Transform the buffered polygon's exterior points back to 4326
    xy = plg_buffered.exterior.coords.xy
    plg_buffered_pnts = [shp.Point(p) for p in list(zip(xy[0], xy[1]))]

    return shp.Polygon(
        [transform(projection_aea_wa_to_4326(), p) for p in plg_buffered_pnts]
    )


def buffer_geometries(geoms, distance, unit):
    if unit == "m":
        buffered_geoms = []
        for geom in geoms:

            if geom.dims == 0:
                # A point
                pnt = shp.Point(geom)
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
    convex_hull = shp.MultiPoint(geoms).convex_hull
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
        shp.MultiPolygon([a.intersection(b) for a, b in combinations(geoms, 2)])
    )

    geom = GEOSGeometry(intersection.wkt)

    return json.dumps(feature_collection([geom]))


def union_geometries(geoms, *args, **kwargs):
    """Calculates the union of the input geometries."""

    mp = shp.MultiPolygon(geoms)
    unary_union_geoms = unary_union(mp)
    union_geom = GEOSGeometry(unary_union_geoms.wkt)

    return json.dumps(feature_collection([union_geom]))


def voronoi(geoms, *args, **kwargs):
    """Calculates the Voronoi diagram of the input geometries."""

    mp = shp.MultiPoint(geoms)
    voronoi = voronoi_diagram(mp)
    voronoi_geom = GEOSGeometry(shp.MultiPolygon(voronoi).wkt)

    return json.dumps(feature_collection([voronoi_geom]))


def centroid(geoms, *args, **kwargs):
    """Calculates the centroid of the input geometries."""

    polygons = []
    for geom in geoms:
        if geom.geom_type == "MultiPolygon":
            polygons += list(geom)
        elif geom.geom_type == "Polygon":
            polygons.append(geom)
        else:
            raise serializers.ValidationError(
                "Centroid operation requires Polygon or MultiPolygon geometries"
            )

    centroid = shp.MultiPolygon(polygons).centroid
    geom = GEOSGeometry(centroid.wkt)

    return json.dumps(feature_collection([geom]))


def mean_center_point(geoms):
    # the mean of the input coordinates (see: https://shapely.readthedocs.io/en/stable/reference/shapely.centroid.html)
    return shp.MultiPoint(geoms).centroid


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


def proxy_object(request_path):
    cache_key = settings.CACHE_KEY_PROXY_NODE_DATA.format(request_path=request_path)
    proxy_dict = cache.get(cache_key)

    if not proxy_dict:
        try:
            proxy = Proxy.objects.get(
                active=True,
                request_path=request_path,
            )
        except Proxy.DoesNotExist:
            raise
        else:
            proxy_dict = {
                "proxy_url": proxy.proxy_url,
                "basic_auth_enabled": proxy.basic_auth_enabled,
                "username": proxy.username,
                "password": proxy.password,
            }
            cache.set(cache_key, proxy_dict, settings.CACHE_TIMEOUT_24_HOURS)

    return proxy_dict


def get_proxy_cache(app_label, model_name):
    cache_key = settings.CACHE_KEY_PROXY_LAYER_DATA.format(
        app_label=app_label, model_name=model_name
    )
    proxy_cache_dumped_data = cache.get(cache_key)
    proxy_cache_array = []

    if proxy_cache_dumped_data is None:
        proxy_cache_query = apps.get_model(app_label, model_name).objects.all()

        for pr in proxy_cache_query:
            proxy_cache_array.append(
                {
                    "layer_name": pr.layer_name,
                    "cache_expiry": 300,
                    "is_external": pr.is_external,
                    "is_internal": pr.is_internal,
                }
            )

        cache.set(cache_key, proxy_cache_array, settings.CACHE_TIMEOUT_24_HOURS)
    else:
        proxy_cache_array = proxy_cache_dumped_data

    return proxy_cache_array


@csrf_exempt
def process_proxy(request, remoteurl, queryString, auth_user, auth_password):
    from django.http import HttpResponse
    from django.core.cache import cache
    from wagov_utils.components.proxy.views import proxy_view
    import base64
    import json

    if request.user.is_authenticated:
        proxy_cache = None
        proxy_response = None
        proxy_response_content = None
        base64_json = {}
        query_string_remote_url = remoteurl + "?" + queryString

        cache_times_strings = get_proxy_cache("boranga", "tilelayer")
        if is_internal(request):
            cache_times_strings = [
                cts for cts in cache_times_strings if cts["is_internal"] is True
            ]
        else:
            cache_times_strings = [
                cts for cts in cache_times_strings if cts["is_external"] is True
            ]

        CACHE_EXPIRY = 300
        layer_allowed = False

        proxy_cache = cache.get(query_string_remote_url)
        query_string_remote_url_new = query_string_remote_url.replace("%3A", ":")
        for cts in cache_times_strings:
            layer_name = cts["layer_name"].split(":")[-1]
            if layer_name in query_string_remote_url:
                CACHE_EXPIRY = cts["cache_expiry"]

            if (
                "?layer=" + cts["layer_name"] in query_string_remote_url_new
                or "&LAYERS=" + cts["layer_name"] in query_string_remote_url_new
            ):
                layer_allowed = True
        if layer_allowed is True:
            if proxy_cache is None:
                auth_details = None
                if auth_user is None and auth_password is None:
                    auth_details = None
                else:
                    auth_details = {"user": auth_user, "password": auth_password}
                proxy_response = proxy_view(request, remoteurl, basic_auth=auth_details)

                # if not is_internal(request):
                #     raise ValidationError("User is not an internal user")

                proxy_response_content_encoded = base64.b64encode(
                    proxy_response.content
                )
                base64_json = {
                    "status_code": proxy_response.status_code,
                    "content_type": proxy_response.headers["content-type"],
                    "content": proxy_response_content_encoded.decode("utf-8"),
                    "cache_expiry": CACHE_EXPIRY,
                }
                if proxy_response.status_code == 200:
                    cache.set(
                        query_string_remote_url, json.dumps(base64_json), CACHE_EXPIRY
                    )
                else:
                    cache.set(query_string_remote_url, json.dumps(base64_json), 15)
            else:
                base64_json = json.loads(proxy_cache)
            proxy_response_content = base64.b64decode(base64_json["content"].encode())
            http_response = HttpResponse(
                proxy_response_content,
                content_type=base64_json["content_type"],
                status=base64_json["status_code"],
            )
            http_response["Django-Cache-Expiry"] = (
                str(base64_json["cache_expiry"]) + " seconds"
            )
            return http_response
        else:
            http_response = HttpResponse(
                "Access Denied", content_type="text/html", status=401
            )
            return http_response
    return
