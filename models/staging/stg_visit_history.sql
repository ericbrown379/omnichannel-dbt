WITH raw_visit_history AS (
    SELECT
        customer_id,
        channel_id,
        visit_timestamp,
        bounce_timestamp,
        CREATED_AT,
        UPDATED_AT
    FROM {{ source("omnichannel", "VisitHistory")}}
)

SELECT
    *
FROM raw_visit_history