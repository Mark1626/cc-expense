{{
  config(
    materialized='view'
  )
}}

SELECT MONTH(date) AS month, SUM(amount) AS expense
    FROM {{ ref('fct_domestic_spending') }}
    GROUP BY category, MONTH(date)
    ORDER BY expense;
