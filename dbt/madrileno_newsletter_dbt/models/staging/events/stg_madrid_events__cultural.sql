with source as (
    select * from {{ source('bronze', 'cultural_events_raw') }}
),

renamed as (
    select
        article_id,
        link as article_url,
        title,
        description,
        keywords,
        creator,
        language,
        country,
        category,
        datatype,
        safe_cast(pubDate as timestamp) as pub_date,
        pubDateTZ as pub_date_tz,
        safe_cast(fetched_at as timestamp) as fetched_at,
        image_url,
        video_url,
        source_id,
        source_name,
        source_priority,
        source_url,
        source_icon,
        duplicate,
        safe_cast(extracted_at as timestamp) as extracted_at
    from source
    where title is not null
)

select * from renamed
