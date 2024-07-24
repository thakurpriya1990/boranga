WITH constants AS (
    SELECT
        'flora' :: VARCHAR(32) AS GroupTypeName,
        ARRAY ['current'] :: VARCHAR(32) [] AS TenureStatusValues,
        ARRAY ['active'] :: VARCHAR(32) [] AS ProcessingStatusValues,
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
occ AS (
    SELECT
        o.id AS id,
        o.occurrence_number AS occurrence_number,
        o.occurrence_name AS occurrence_name,
        o.processing_status AS processing_status,
        o.group_type_id AS group_type_id,
        o.species_id AS species_id,
        o.community_id AS community_id,
        o.wild_status_id AS wild_status_id,
        MAX(r.observation_date) AS ocr_ob_dat
    FROM
        boranga_occurrence o
        LEFT JOIN boranga_occurrencereport r ON r.occurrence_id = o.id,
        constants
    WHERE
        o.processing_status = ANY(constants.ProcessingStatusValues)
    GROUP BY
        o.id
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
        sd.id AS species_distribution_id,
        sd.extent_of_occurrences AS extent_of_occurrences,
        sd.area_of_occupancy AS area_of_occupancy,
        sd.area_of_occupancy_actual AS area_of_occupancy_actual,
        wal.id AS wa_legislative_list_id,
        wal.label AS wa_legislative_list_label,
        wal.code AS wa_legislative_list_code,
        string_agg(distinct(walc.code), ',') AS wa_legislative_category_codes,
        string_agg(distinct(wapc.code), ',') AS wa_priority_category_codes
    FROM
        boranga_species s
        LEFT JOIN boranga_taxonomy t ON s.taxonomy_id = t.id
        LEFT JOIN boranga_taxonvernacular tv ON s.taxonomy_id = tv.taxonomy_id
        LEFT JOIN boranga_speciesdistribution sd ON s.id = sd.species_id
        LEFT JOIN cs ON s.id = cs.species_id
        LEFT JOIN boranga_walegislativelist wal ON cs.wa_legislative_list_id = wal.id
        LEFT JOIN boranga_walegislativecategory_wa_legislative_lists wac_wal ON wac_wal.walegislativecategory_id = cs.wa_legislative_category_id
        LEFT JOIN boranga_walegislativecategory walc ON walc.id = wac_wal.walegislativecategory_id
        LEFT JOIN boranga_waprioritycategory_wa_priority_lists wap_wal ON wap_wal.waprioritycategory_id = cs.wa_priority_category_id
        LEFT JOIN boranga_waprioritycategory wapc ON wapc.id = wap_wal.waprioritycategory_id
    GROUP BY
        s.id,
        t.scientific_name,
        tv.vernacular_name,
        sd.id,
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
),
wildstatus AS (
    SELECT
        ws.id,
        ws.name AS wild_status_name
    FROM
        boranga_wildstatus ws
),
loc AS (
    SELECT
        l.id,
        l.occurrence_id,
        r.name AS region_name,
        d.name AS district_name,
        d.code AS district_code,
        l.locality,
        l.location_description,
        l.boundary_description,
        cs.name AS coordinate_source_name,
        la.name AS location_accuracy_name
    FROM
        boranga_occlocation l
        LEFT JOIN boranga_region r ON l.region_id = r.id
        LEFT JOIN boranga_district d ON l.district_id = d.id
        LEFT JOIN boranga_coordinatesource cs ON l.coordinate_source_id = cs.id
        LEFT JOIN boranga_locationaccuracy la ON l.location_accuracy_id = la.id
),
identification AS (
    SELECT
        i.id,
        c.name AS identification_certainty_name
    FROM
        boranga_occidentification i
        LEFT JOIN boranga_identificationcertainty c ON i.identification_certainty_id = c.id
),
geom AS (
    SELECT
        og.id AS id,
        CASE
            ST_GeometryType(geometry)
            WHEN 'ST_Point' THEN ST_Buffer(geometry, 0.00001)
            WHEN 'ST_MultiPoint' THEN ST_Buffer(geometry, 0.00001)
            ELSE geometry
        END AS geometry,
        ST_GeometryType(geometry) AS geometry_type,
        occurrence_id,
        'occurrence geometry' AS data_type,
        buffer_radius,
        'ID,Status,Purpose,Vesting; ' || string_agg(
            distinct(
                concat_ws(
                    ',',
                    otc.tenure_area_id,
                    otc.status,
                    coalesce(p.code, ''),
                    coalesce(v.code, '')
                )
            ),
            '; '
        ) AS occurrence_tenures
    FROM
        boranga_occurrencegeometry og
        LEFT JOIN boranga_occurrencetenure otc ON otc.occurrence_geometry_id = og.id
        OR otc.historical_occurrence = og.occurrence_id
        LEFT JOIN boranga_occurrencetenurepurpose p ON p.id = otc.purpose_id
        LEFT JOIN boranga_occurrencetenurevesting v ON v.id = otc.vesting_id,
        constants
    GROUP BY
        og.id,
        otc.status,
        constants.TenureStatusValues
    HAVING
        otc.status = ANY(constants.TenureStatusValues)
    UNION
    SELECT
        bg.id AS id,
        bg.geometry AS geometry,
        ST_GeometryType(bg.geometry) AS geometry_type,
        og.occurrence_id AS occurrence_id,
        'buffer geometry' AS data_type,
        0 as buffer_radius,
        '' AS occurrence_tenures
    FROM
        boranga_buffergeometry bg
        INNER JOIN boranga_occurrencegeometry og ON og.id = bg.buffered_from_geometry_id
)
SELECT
    occ.occurrence_number AS occ_id,
    occ.occurrence_name AS occ_name,
    gt.name AS group_type,
    geom.geometry AS geometry,
    geom.geometry_type AS geom_type,
    geom.data_type AS g_datatype,
    geom.buffer_radius AS buff_value,
    geom.occurrence_tenures AS tenures,
    species.species_number AS species_id,
    species.scientific_name AS scien_name,
    species.vernacular_name AS vern_name,
    species.extent_of_occurrences AS ext_occ,
    species.area_of_occupancy AS area_occ,
    species.area_of_occupancy_actual AS aoo_actual,
    species.wa_legislative_list_label AS cs_ls_labl,
    species.wa_legislative_list_code AS cs_ls_code,
    species.wa_legislative_category_codes AS cs_leg_cat,
    species.wa_priority_category_codes AS cs_pr_cat,
    community.community_number AS communi_id,
    community.community_name AS commu_name,
    wildstatus.wild_status_name AS wld_status,
    loc.region_name AS region,
    loc.district_name AS district,
    loc.district_code AS distr_code,
    loc.locality AS locality,
    loc.location_description AS loc_desc,
    loc.boundary_description AS bound_desc,
    loc.coordinate_source_name AS coord_src,
    loc.location_accuracy_name AS loc_acc,
    ic.name AS ident_crty,
    pc.count_date AS pl_cnt_dat,
    pc.simple_alive AS pl_smp_alv,
    pc.detailed_alive_mature AS pl_alv_mat,
    ao.count_date AS an_cnt_dat,
    ao.alive_adult_male + ao.alive_adult_female + ao.alive_adult_unknown + ao.alive_juvenile_male + ao.alive_juvenile_female + ao.alive_juvenile_unknown + ao.alive_unsure_male + ao.alive_unsure_female + ao.alive_unsure_unknown AS an_alive,
    occ.ocr_ob_dat AS ocr_ob_dat
FROM
    occ
    RIGHT JOIN geom ON occ.id = geom.occurrence_id
    JOIN gt ON occ.group_type_id = gt.id
    LEFT JOIN species ON occ.species_id = species.id
    LEFT JOIN community ON occ.community_id = community.id
    LEFT JOIN wildstatus ON occ.wild_status_id = wildstatus.id
    LEFT JOIN loc ON occ.id = loc.occurrence_id
    LEFT JOIN boranga_occidentification i ON occ.id = i.occurrence_id
    LEFT JOIN boranga_identificationcertainty ic ON i.identification_certainty_id = ic.id
    LEFT JOIN boranga_occplantcount pc ON occ.id = pc.occurrence_id
    LEFT JOIN boranga_occanimalobservation ao ON occ.id = ao.occurrence_id
    LEFT JOIN boranga_occhabitatcondition hc ON occ.id = hc.occurrence_id
WHERE
    occ.group_type_id = gt.id;