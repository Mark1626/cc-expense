{{
  config(
    materialized='table'
  )
}}

SELECT 
    CASE
        -- Match date and time
        WHEN column1 ~ '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/([0-9]{4}) ([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$'
        THEN strptime(column1, '%d/%m/%Y %H:%M:%S')
        
        -- Match date only
        WHEN column1 ~ '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/([0-9]{4})$'
        THEN strptime(column1 || ' 00:00:00', '%d/%m/%Y %H:%M:%S')
        
        ELSE NULL
    END AS date,

    column2 as description,

    CAST(regexp_replace(
        regexp_extract(column4, '^[0-9,]+(\.[0-9]+)?$', 0),
    ',', '') AS DECIMAL(12,2)) AS amount
FROM {{ ref('stg_domestic_data_raw') }}
WHERE date IS NOT NULL AND
    column4 NOT LIKE '%Cr%' AND
    TRY_CAST(regexp_replace(column4, ',', '') AS DECIMAL(12,2)) IS NOT NULL
