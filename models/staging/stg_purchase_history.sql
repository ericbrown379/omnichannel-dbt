WITH raw_purchase_history AS (
    SELECT
        customer_id,
        product_sku,
        channel_id,
        quantity,
        discount,
        order_date
    FROM {{ source("omnichannel", "PurchaseHistory")}}
)

SELECT
    *
FROM raw_purchase_history