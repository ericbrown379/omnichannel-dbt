WITH base_cte AS 
(
    SELECT
        dp.dsc_product_name,
        dc.dsc_channel_name,
        ROUND(SUM(fct.mtr_total_amount_net), 2) AS sum_total_amount
    FROM {{ ref("fct_purchase_history") }} AS fct
    LEFT JOIN {{ ref("dim_products") }} AS dp
            ON dp.sk_product = fct.sk_product
    LEFT JOIN {{ ref("dim_channels") }} AS dc
            ON dc.sk_channel = fct.sk_channel
    GROUP BY dc.dsc_channel_name, dp.dsc_product_name
),
ranked_cte AS 
(
    SELECT 
        base_cte.dsc_product_name,
        base_cte.dsc_channel_name,
        base_cte.sum_total_amount,
        RANK() OVER (PARTITION BY dsc_channel_name 
        ORDER BY sum_total_amount DESC) AS rank_total_amount
    FROM base_cte
)
SELECT *
FROM ranked_cte
WHERE rank_total_amount <= 3;