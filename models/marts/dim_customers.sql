WITH stg_dim_customers AS 
(
    SELECT
        customer_id AS nk_customer_id,
        name AS dsc_name,
        date_birth AS dt_date_birth,
        email_address AS dsc_email_address,
        phone_number AS dsc_phone_number,
        country AS dsc_country,
        CREATED_AT AS dt_created_at,
        UPDATED_AT AS dt_updated_at
    FROM {{ ref("stg_customers")}}
)

SELECT
    {{ dbt_utils.generate_surrogate_key( ["nk_customer_id"] )}} AS sk_customer,
    *
FROM stg_dim_customers