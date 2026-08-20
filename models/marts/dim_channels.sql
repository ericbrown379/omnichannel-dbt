WITH stg_dim_channels AS 
(
    SELECT
        channel_id AS nk_channel_id,
        channel_name AS dsc_channel_name,
        CREATED_AT dt_created_at,
        UPDATED_AT AS dt_updated_at
    FROM {{ ref("stg_channels")}}
)

SELECT
    {{ dbt_utils.generate_surrogate_key( ["nk_channel_id"] )}} AS sk_channel,
    *
FROM stg_dim_channels