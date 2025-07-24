{{
  config(
    materialized='view'
  )
}}

SELECT * FROM {{ ref('fct_domestic_spending') }} WHERE category='Other';
