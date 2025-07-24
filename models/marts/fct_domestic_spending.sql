{{
  config(
    materialized='table'
  )
}}

WITH base_data AS (
  SELECT 
    date,
    description,
    amount,
    LOWER(description) AS normalized_description
  FROM {{ ref('stg_domestic_data_cleaned') }}
),
joined_data AS (
  SELECT
    b.*,
    m.category,
    m.subcategory,
    m.description_pattern
  FROM base_data b
  LEFT JOIN {{ ref('description_categories') }} m
    ON b.normalized_description LIKE '%' || LOWER(m.description_pattern) || '%'
),
ranked_data AS(
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY date, description, amount 
                        ORDER BY LENGTH(description_pattern) DESC) AS rn
  FROM joined_data
)

SELECT
  date,
  description,
  amount,
  COALESCE(category, 'Other') AS category,
  COALESCE(subcategory, 'Other') AS subcategory
FROM ranked_data
WHERE rn = 1
