SELECT
    dd.year_number,
    dd.quarter_of_year,
    ROUND(SUM(fct.mtr_total_amount_net), 2) AS sum_total_amount_with_discount
FROM {{ ref("fct_purchase_history") }} AS fct
LEFT JOIN {{ ref("dim_date") }} AS dd
        ON dd.date_day = fct.sk_order_date
GROUP BY dd.year_number, dd.quarter_of_year