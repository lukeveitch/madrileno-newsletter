with source as (
    select * from {{ source('bronze', 'news_articles_raw') }}
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
        date(safe_cast(pubDate as timestamp)) as pub_date_date,
        time(safe_cast(pubDate as timestamp)) as pub_date_time,
        pubDateTZ as pub_date_tz,
        safe_cast(fetched_at as timestamp) as fetched_at,
        date(safe_cast(fetched_at as timestamp)) as fetched_at_date,
        time(safe_cast(fetched_at as timestamp)) as fetched_at_time,
        image_url,
        video_url,
        source_id,
        source_name,
        source_priority,
        source_url,
        source_icon,
        duplicate,
        safe_cast(extracted_at as timestamp) as extracted_at,
        date(safe_cast(extracted_at as timestamp)) as extracted_at_date,
        time(safe_cast(extracted_at as timestamp)) as extracted_at_time
    from source
    where title is not null
)

select * from renamed
