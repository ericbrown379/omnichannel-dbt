SELECT
    sk_customer,
    sk_channel,
    sk_product,
    SUM(mtr_total_amount_gross) AS mtr_total_amount_gross,
    SUM(mtr_unit_price) AS mtr_unit_price
FROM {{ ref('fct_purchase_history') }}
GROUP BY 1, 2, 3
HAVING mtr_unit_price > mtr_total_amount_gross