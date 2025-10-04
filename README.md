# CC Expense Tracking

## Preprocessing

```
uv run python ./scripts/parse_regalia_statement.py <glob-pattern>
```

## Running the pipeline

```
dbt seed
dbt run --select your_model --vars '{"domestic_data_path": "new/path/raw_data_domestic_*.csv"}'
```

## Analysis

```
uv run marimo edit analysis.py
```
