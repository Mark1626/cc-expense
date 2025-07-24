{{
  config(
    materialized='table'
  )
}}

SELECT * FROM read_csv('{{ var("domestic_data_path") }}', all_varchar=true)
