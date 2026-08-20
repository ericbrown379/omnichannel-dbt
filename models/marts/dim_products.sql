WITH stg_dim_products AS 
(
    SELECT
        product_sku AS nk_product_sku,
        product_name AS dsc_product_name,
        unit_price AS mtr_unit_price,
        CREATED_AT AS dt_created_at,
        UPDATED_AT AS dt_updated_at
    FROM {{ ref("stg_products")}}
)

SELECT
    {{ dbt_utils.generate_surrogate_key( ["nk_product_sku"] )}} AS sk_product,
    *
FROM stg_dim_products