WITH constants AS (
    SELECT
        'community' :: VARCHAR(32) AS GroupTypeName,
        ARRAY ['approved'] :: VARCHAR(32) [] AS ProcessingStatusValues,
        ARRAY ['approved'] :: VARCHAR(32) [] AS ConservationStatusStatusValues
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
        o.id AS id,
        o.occurrence_report_number AS occurrence_report_number,
        o.occurrence_id AS occurrence_id,
        o.processing_status AS processing_status,
        o.group_type_id AS group_type_id,
        o.species_id AS species_id,
        o.community_id AS community_id,
        o.observation_date AS observation_date,
        o.reported_date AS reported_date,
        o.lodgement_date AS lodgement_date,
        o.site AS site,
        string_agg(distinct(od.observer_name), ',') AS observer_name,
        bool_and(od.main_observer) AS main_observer,
        string_agg(distinct(od.organisation), ',') AS organisation
    FROM
        boranga_occurrencereport o
        LEFT JOIN boranga_ocrobserverdetail od ON o.id = od.occurrence_report_id
        AND od.main_observer = TRUE,
        constants
    WHERE
        o.processing_status = ANY(constants.ProcessingStatusValues)
    GROUP BY
        o.id
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
        cs.name AS coordinate_source_name,
        la.name AS location_accuracy_name
    FROM
        boranga_ocrlocation l
        LEFT JOIN boranga_region r ON l.region_id = r.id
        LEFT JOIN boranga_district d ON l.district_id = d.id
        LEFT JOIN boranga_coordinatesource cs ON l.coordinate_source_id = cs.id
        LEFT JOIN boranga_locationaccuracy la ON l.location_accuracy_id = la.id
),
geom AS (
    SELECT
        id,
        TO_CHAR(updated_date, 'YYYY-MM-DD HH:MM:SS') AS updated,
        CASE
            ST_GeometryType(geometry)
            WHEN 'ST_Point' THEN ST_Buffer(geometry, 0.00001)
            WHEN 'ST_MultiPoint' THEN ST_Buffer(geometry, 0.00001)
            ELSE geometry
        END AS geometry,
        ST_GeometryType(geometry) AS geometry_type,
        occurrence_report_id,
        'occurrence report geometry' AS data_type,
        ROUND(
            ST_Area(ST_Transform(geometry, 4326) :: geography)
        ) AS area_sqm
    FROM
        boranga_occurrencereportgeometry
),
cs AS (
    SELECT
        cs.id,
        cs.species_id,
        cs.wa_legislative_list_id,
        cs.wa_legislative_category_id,
        cs.wa_priority_category_id
    FROM
        boranga_conservationstatus cs,
        constants
    WHERE
        cs.processing_status = ANY(constants.ConservationStatusStatusValues)
),
species AS (
    SELECT
        s.id,
        s.species_number AS species_number,
        s.taxonomy_id AS taxonomy_id,
        t.scientific_name AS scientific_name,
        tv.vernacular_name AS vernacular_name,
        wal.id AS wa_legislative_list_id,
        wal.label AS wa_legislative_list_label,
        wal.code AS wa_legislative_list_code,
        string_agg(distinct(walc.code), ',') AS wa_legislative_category_codes,
        string_agg(distinct(wapc.code), ',') AS wa_priority_category_codes
    FROM
        boranga_species s
        LEFT JOIN boranga_taxonomy t ON s.taxonomy_id = t.id
        LEFT JOIN boranga_taxonvernacular tv ON s.taxonomy_id = tv.taxonomy_id
        LEFT JOIN cs ON s.id = cs.species_id
        LEFT JOIN boranga_walegislativelist wal ON cs.wa_legislative_list_id = wal.id
        LEFT JOIN boranga_walegislativecategory wac ON cs.wa_legislative_category_id = wac.id
        LEFT JOIN boranga_walegislativecategory_wa_legislative_lists wac_wal ON wac_wal.walegislativecategory_id = cs.wa_legislative_category_id
        LEFT JOIN boranga_walegislativecategory walc ON walc.id = wac_wal.walegislativecategory_id
        LEFT JOIN boranga_waprioritycategory_wa_priority_lists wap_wal ON wap_wal.waprioritycategory_id = cs.wa_priority_category_id
        LEFT JOIN boranga_waprioritycategory wapc ON wapc.id = wap_wal.waprioritycategory_id
    GROUP BY
        s.id,
        t.scientific_name,
        tv.vernacular_name,
        wal.id
),
community AS (
    SELECT
        c.id,
        c.community_number AS community_number,
        ct.community_name AS community_name
    FROM
        boranga_community c
        LEFT JOIN boranga_communitytaxonomy ct ON c.id = ct.community_id
)
SELECT
    ocr.occurrence_report_number AS ocr_id,
    occ.occurrence_number AS occ_id,
    gt.name AS group_type,
    geom.geometry AS geometry,
    geom.updated AS updated,
    geom.geometry_type AS geom_type,
    geom.area_sqm AS g_area_sqm,
    geom.data_type AS g_data_type,
    species.species_number AS species_id,
    species.scientific_name AS scien_name,
    species.vernacular_name AS vern_name,
    species.wa_legislative_list_label AS cs_ls_labl,
    species.wa_legislative_list_code AS cs_ls_code,
    species.wa_legislative_category_codes AS cd_leg_cat,
    species.wa_priority_category_codes AS cd_pr_cat,
    community.community_number AS communi_id,
    community.community_name AS commu_name,
    ocr.observation_date AS obs_date,
    ocr.reported_date AS rep_date,
    ocr.lodgement_date AS lodg_date,
    ocr.site AS ocr_site,
    loc.region_name AS region,
    loc.district_name AS district,
    loc.district_code AS distr_code,
    loc.locality AS locality,
    loc.location_description AS loc_desc,
    loc.boundary_description AS bound_desc,
    loc.coordinate_source_name AS coord_src,
    loc.location_accuracy_name AS loc_acc,
    ic.name AS ident_crty,
    ocr.observer_name AS obs_name,
    ocr.main_observer AS main_obs,
    ocr.organisation AS organistn,
    pc.count_date AS pl_cnt_dat,
    pc.simple_alive AS pl_smp_alv,
    pc.detailed_alive_mature AS pl_alv_mat,
    ao.count_date AS an_cnt_dat,
    ao.alive_adult_male + ao.alive_adult_female + ao.alive_adult_unknown + ao.alive_juvenile_male + ao.alive_juvenile_female + ao.alive_juvenile_unknown + ao.alive_unsure_male + ao.alive_unsure_female + ao.alive_unsure_unknown AS an_alive
FROM
    ocr
    RIGHT JOIN geom ON ocr.id = geom.occurrence_report_id
    JOIN gt ON ocr.group_type_id = gt.id
    LEFT JOIN occ ON ocr.occurrence_id = occ.id
    LEFT JOIN species ON ocr.species_id = species.id
    LEFT JOIN community ON ocr.community_id = community.id
    LEFT JOIN loc ON ocr.id = loc.occurrence_report_id
    LEFT JOIN boranga_ocridentification i ON occ.id = i.occurrence_report_id
    LEFT JOIN boranga_identificationcertainty ic ON i.identification_certainty_id = ic.id
    LEFT JOIN boranga_ocrplantcount pc ON ocr.id = pc.occurrence_report_id
    LEFT JOIN boranga_ocranimalobservation ao ON ocr.id = ao.occurrence_report_id
WHERE
    ocr.group_type_id = gt.id;