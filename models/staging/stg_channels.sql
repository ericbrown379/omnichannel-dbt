WITH raw_channels AS (
    SELECT
        channel_id,
        channel_name,
        CREATED_AT,
        UPDATED_AT
    FROM {{ source("omnichannel", "Channels")}}

)

SELECT
    *
FROM raw_channels