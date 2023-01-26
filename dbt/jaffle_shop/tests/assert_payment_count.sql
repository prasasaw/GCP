select
    count(*) as cnt
from {{ ref('stg_payments' )}}
having (cnt <= 150)
