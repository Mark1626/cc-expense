{{
  config(
    materialized='view'
  )
}}

SELECT category, sum(amount) as amount FROM {{ ref('fct_domestic_spending') }}
      GROUP BY category
      ORDER BY amount DESC;
