SELECT 
    dc.dsc_channel_name,
    ROUND(AVG(mtr_length_of_stay_minutes), 2) AS avg_length_of_stay_minutes
FROM {{ ref("fct_visit_history") }} AS fct
LEFT JOIN {{ ref("dim_channels") }} AS dc
        ON dc.sk_channel = fct.sk_channel
GROUP BY dc.dsc_channel_name