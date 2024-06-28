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
        lodgement_date,
        site
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
loc AS (
    SELECT
        l.id,
        l.occurrence_report_id,
        r.name AS region_name,
        d.name AS district_name,
        d.code AS district_code,
        l.locality,
        l.location_description,
        l.boundary_description,
        cs.name AS coordination_source_name,
        la.name AS location_accuracy_name
    FROM
        boranga_ocrlocation l
        LEFT JOIN boranga_region r ON l.region_id = r.id
        LEFT JOIN boranga_district d ON l.district_id = d.id
        LEFT JOIN boranga_coordinationsource cs ON l.coordination_source_id = cs.id
        LEFT JOIN boranga_locationaccuracy la ON l.location_accuracy_id = la.id
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
    ocr.occurrence_report_number AS ocr_number,
    occ.occurrence_number AS occ_number,
    gt.name AS group_type,
    geom.geometry AS geometry,
    geom.geometry_type AS geom_type,
    geom.data_type AS g_data_type,
    species.species_number AS species_nr,
    community.community_number AS commnty_nr,
    ocr.observation_date AS obs_date,
    ocr.reported_date AS rep_date,
    ocr.lodgement_date AS lodg_date,
    ocr.site AS site,
    loc.locality AS locality,
    loc.location_description AS loc_desc,
    loc.boundary_description AS bound_desc
FROM
    ocr
    RIGHT JOIN geom ON ocr.id = geom.occurrence_report_id
    JOIN gt ON ocr.group_type_id = gt.id
    LEFT JOIN occ ON ocr.occurrence_id = occ.id
    LEFT JOIN species ON ocr.species_id = species.id
    LEFT JOIN community ON ocr.community_id = community.id
    LEFT JOIN loc ON ocr.id = loc.occurrence_report_id
WHERE
    ocr.group_type_id = gt.id;