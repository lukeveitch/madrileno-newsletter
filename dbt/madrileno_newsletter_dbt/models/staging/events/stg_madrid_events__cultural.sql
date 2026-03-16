with source as (
    select * from {{ source('bronze', 'cultural_events_raw') }}
),

renamed as (
    select
        at_id,
        at_type,
        id,
        title,
        description,
        free,
        safe_cast(price as float64) as price,
        dtstart,
        date(safe_cast(dtstart as timestamp)) as dtstart_date,
        dtend,
        time(safe_cast(dtend as timestamp)) as dtend_time,
        time as time_label,
        excluded_days,
        uid,
        link as event_url,
        event_location,
        safe_cast(extracted_at as timestamp) as extracted_at,
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
        audience
    from source
    where title is not null
)

select * from renamed
