# CC Expense Tracking

## Running the pipeline

```
dbt seed
dbt run --select your_model --vars '{"domestic_data_path": "new/path/raw_data_domestic_*.csv"}'
```
