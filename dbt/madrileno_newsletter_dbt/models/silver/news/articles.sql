select *
from {{ ref('stg_newsdata__articles') }}