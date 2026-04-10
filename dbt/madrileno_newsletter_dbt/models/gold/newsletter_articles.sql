with recent as (
    select
        title,
        description,
        article_url,
        source_name,
        pub_date,
        pub_date_date,
        category,
        keywords,
        image_url,
        language,
        country
    from {{ ref('articles') }}
    where pub_date_date = current_date
)

select * from recent
order by pub_date desc
