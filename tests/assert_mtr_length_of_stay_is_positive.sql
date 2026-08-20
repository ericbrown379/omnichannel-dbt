SELECT
    sk_customer,
    sk_channel,
    SUM(mtr_length_of_stay_minutes) AS mtr_length_of_stay_minutes
FROM {{ ref('fct_visit_history') }}
GROUP BY 1, 2
HAVING mtr_length_of_stay_minutes < 0