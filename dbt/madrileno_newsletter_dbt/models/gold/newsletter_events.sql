with upcoming as (
    select
        title,
        description,
        free,
        price,
        dtstart_date,
        dtstart,
        dtend_time,
        time_label,
        event_url,
        event_location,
        address_area_street_address,
        address_area_locality,
        address_area_postal_code,
        location_latitude,
        location_longitude,
        organization_organization_name,
        event_source
    from {{ ref('all_events') }}
    where dtstart_date between current_date and date_add(current_date, interval 7 day)
)

select * from upcoming
order by dtstart_date asc
