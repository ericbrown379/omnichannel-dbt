WITH base_cte AS 
(
    SELECT
        dcu.dsc_name,
        dcu.dsc_email_address,
        dc.dsc_channel_name,
        ROUND(SUM(fct.mtr_total_amount_net), 2) AS sum_total_amount
    FROM {{ ref("fct_purchase_history") }} AS fct
    LEFT JOIN {{ ref("dim_customers") }} AS dcu
            ON dcu.sk_customer = fct.sk_customer
    LEFT JOIN {{ ref("dim_channels") }} AS dc
            ON dc.sk_channel = fct.sk_channel
    WHERE dc.dsc_channel_name = 'Mobile App'
        AND EXTRACT(YEAR FROM fct.sk_order_date) = 2023
    GROUP BY dcu.dsc_name, dcu.dsc_email_address, dc.dsc_channel_name
    ORDER BY sum_total_amount DESC
)
SELECT *
FROM base_cte
LIMIT 3;