with cultural as (
    select
        at_id,
        at_type,
        id,
        title,
        description,
        free,
        price,
        dtstart,
        dtstart_date,
        dtend,
        dtend_time,
        time_label,
        excluded_days,
        uid,
        event_url,
        event_location,
        extracted_at,
        recurrence_days,
        recurrence_frequency,
        recurrence_interval,
        references_at_id,
        relation_at_id,
        address_district_at_id,
        address_area_at_id,
        address_area_locality,
        address_area_postal_code,
        address_area_street_address,
        location_latitude,
        location_longitude,
        organization_organization_name,
        organization_accesibility,
        'cultural' as event_source
    from {{ ref('stg_madrid_events__cultural') }}
    where dtstart_date >= current_date
),

general as (
    select
        at_id,
        at_type,
        id,
        title,
        description,
        free,
        price,
        dtstart,
        dtstart_date,
        dtend,
        dtend_time,
        time_label,
        excluded_days,
        uid,
        event_url,
        event_location,
        extracted_at,
        recurrence_days,
        recurrence_frequency,
        recurrence_interval,
        references_at_id,
        relation_at_id,
        address_district_at_id,
        address_area_at_id,
        address_area_locality,
        address_area_postal_code,
        address_area_street_address,
        location_latitude,
        location_longitude,
        organization_organization_name,
        organization_accesibility,
        'general' as event_source
    from {{ ref('stg_madrid_events__general') }}
    where dtstart_date >= current_date
),

unioned as (
    select * from cultural
    union all
    select * from general
),

deduplicated as (
    select *
    from unioned
    qualify row_number() over (
        partition by at_id
        order by extracted_at desc
    ) = 1
)

select * from deduplicated
