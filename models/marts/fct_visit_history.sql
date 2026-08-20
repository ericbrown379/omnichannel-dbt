WITH stg_fct_visit_history AS 
(
    SELECT
        customer_id AS nk_customer_id,
        channel_id AS nk_channel_id,
        CAST(visit_timestamp AS DATE) AS sk_date_visit,
        CAST(bounce_timestamp AS DATE) AS sk_date_bounce,
        CAST(visit_timestamp AS DATETIME) AS dt_visit_timestamp,
        CAST(bounce_timestamp AS DATETIME) AS dt_bounce_timestamp
    FROM {{ ref("stg_visit_history")}}
)

SELECT
    coalesce(dcust.sk_customer, '-1') AS sk_customer,
    coalesce(dchan.sk_channel, '-1') AS sk_channel,
    fct.sk_date_visit,
    fct.sk_date_bounce,
    fct.dt_visit_timestamp,
    fct.dt_bounce_timestamp,
    DATE_DIFF(fct.dt_bounce_timestamp, fct.dt_visit_timestamp
    , MINUTE) AS mtr_length_of_stay_minutes
FROM stg_fct_visit_history AS fct
LEFT JOIN {{ ref("dim_customers") }} AS dcust 
            ON fct.nk_customer_id = dcust.nk_customer_id
LEFT JOIN {{ ref("dim_channels") }} AS dchan 
            ON fct.nk_channel_id = dchan.nk_channel_id