WITH constants AS (
    SELECT
        'fauna' :: VARCHAR(32) AS GroupTypeName,
        ARRAY ['active'] :: VARCHAR(32) [] AS ProcessingStatusValues
),
gt AS (
    SELECT
        id,
        name
    FROM
        boranga_grouptype,
        constants
    WHERE
        name = constants.GroupTypeName
),
occ AS (
    SELECT
        id,
        occurrence_number,
        occurrence_name,
        processing_status,
        group_type_id
    FROM
        boranga_occurrence,
        constants
    WHERE
        processing_status = ANY(constants.ProcessingStatusValues)
),
geom AS (
    SELECT
        id,
        CASE
            ST_GeometryType(geometry)
            WHEN 'ST_Point' THEN ST_Buffer(geometry, 0.00001)
            ELSE geometry
        END AS geometry,
        ST_GeometryType(geometry) AS geometry_type,
        occurrence_id,
        'occurrence geometry' AS data_type
    FROM
        boranga_occurrencegeometry
    UNION
    SELECT
        bg.id AS id,
        bg.geometry AS geometry,
        ST_GeometryType(bg.geometry) AS geometry_type,
        og.occurrence_id AS occurrence_id,
        'buffer geometry' AS data_type
    FROM
        boranga_buffergeometry bg
        INNER JOIN boranga_occurrencegeometry og ON og.id = bg.buffered_from_geometry_id
)
SELECT
    occ.occurrence_number,
    occ.occurrence_name AS occ_name,
    gt.name AS group_type,
    geom.geometry AS geometry,
    geom.geometry_type AS geom_type,
    geom.data_type AS g_datatype
FROM
    occ
    RIGHT JOIN geom ON occ.id = geom.occurrence_id
    JOIN gt ON occ.group_type_id = gt.id
WHERE
    occ.group_type_id = gt.id;