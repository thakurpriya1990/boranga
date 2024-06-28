WITH constants AS (
    SELECT
        'flora' :: VARCHAR(32) AS GroupTypeName,
        ARRAY ['approved'] :: VARCHAR(32) [] AS ProcessingStatusValues
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
ocr AS (
    SELECT
        id,
        occurrence_report_number,
        occurrence_id,
        processing_status,
        group_type_id,
        species_id,
        community_id,
        observation_date,
        reported_date,
        lodgement_date
    FROM
        boranga_occurrencereport,
        constants
    WHERE
        processing_status = ANY(constants.ProcessingStatusValues)
),
occ AS (
    SELECT
        id,
        occurrence_number
    FROM
        boranga_occurrence
),
geom AS (
    SELECT
        id,
        CASE
            ST_GeometryType(geometry)
            WHEN 'ST_Point' THEN ST_Buffer(geometry, 0.00001) -- 0.00001 deg ~= 1.1m
            ELSE geometry
        END AS geometry,
        ST_GeometryType(geometry) AS geometry_type,
        occurrence_report_id,
        'occurrence report geometry' AS data_type
    FROM
        boranga_occurrencereportgeometry
),
species AS (
    SELECT
        id,
        species_number,
        taxonomy_id
    FROM
        boranga_species
),
community AS (
    SELECT
        id,
        community_number
    FROM
        boranga_community
)
SELECT
    ocr.occurrence_report_number,
    occ.occurrence_number,
    gt.name AS group_type,
    geom.geometry AS geometry,
    geom.geometry_type AS geometry_type,
    geom.data_type AS geometry_data_type,
    species.species_number AS species_number,
    community.community_number AS community_number,
    ocr.observation_date,
    ocr.reported_date,
    ocr.lodgement_date
FROM
    ocr
    RIGHT JOIN geom ON ocr.id = geom.occurrence_report_id
    JOIN gt ON ocr.group_type_id = gt.id
    LEFT JOIN occ ON ocr.occurrence_id = occ.id
    LEFT JOIN species ON ocr.species_id = species.id
    LEFT JOIN community ON ocr.community_id = community.id
WHERE
    ocr.group_type_id = gt.id;