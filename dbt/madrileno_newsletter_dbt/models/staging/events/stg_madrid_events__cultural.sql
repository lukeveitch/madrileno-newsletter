with source as (
    select * from {{ source('bronze', 'cultural_events_raw') }}
),

renamed as (
    select
        article_id as id,
        * except(article_id)
    from source
)