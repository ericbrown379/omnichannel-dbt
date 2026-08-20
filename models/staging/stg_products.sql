WITH raw_products AS (
    SELECT
        product_sku,
        product_name,
        unit_price,
        CREATED_AT,
        UPDATED_AT
    FROM {{ source("omnichannel", "Products")}}
)


SELECT
    *
FROM raw_products