import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import altair as alt
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    return mo, plt, sns


@app.cell
def _():
    import duckdb

    DATABASE_URL = "/path/to/db"
    engine = duckdb.connect(DATABASE_URL, read_only=True)
    return (engine,)


@app.cell
def _(mo):
    mo.md(r"""## Top 10 expenses""")
    return


@app.cell
def _(engine, fct_domestic_spending, mo):
    _df = mo.sql(
        f"""
        SELECT
            *
        FROM
            fct_domestic_spending
        order by
            amount desc,
            date desc
        limit
            10;
        """,
        engine=engine
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## Monthly expense trend""")
    return


@app.cell
def _(engine, plt, sns):
    monthly_expenses = engine.execute("""
        SELECT 
            strftime(date, '%Y-%m') as month,
            SUM(amount) as total_expenses
        FROM fct_domestic_spending
        GROUP BY month
        ORDER BY month
    """).df()

    # Plot
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_expenses, x='month', y='total_expenses', marker='o')
    plt.title('Monthly Expense Trend')
    plt.xlabel('Month')
    plt.ylabel('Total Expenses')
    plt.xticks(rotation=45)
    plt.tight_layout()
    for i, row in monthly_expenses.iterrows():
        plt.text(row['month'], row['total_expenses'] * 1.02, f"Rs: {row['total_expenses']:,.0f}", 
                 ha='center', va='bottom', fontsize=9)
    plt.show()
    return


@app.cell
def _(mo):
    mo.md(r"""## Expense by Category""")
    return


@app.cell
def _(engine, plt):
    category_expenses = engine.execute("""
        SELECT 
            category,
            SUM(amount) as total_expenses
        FROM fct_domestic_spending
        GROUP BY category
        ORDER BY total_expenses DESC
    """).df()

    # Plot
    plt.figure(figsize=(8, 8))
    plt.pie(category_expenses['total_expenses'], 
            labels=category_expenses['category'],
            autopct='%1.1f%%')
    plt.title('Expense Distribution by Category')
    plt.show()

    return


@app.cell
def _(mo):
    mo.md(r"""### Expense by Sub - category""")
    return


@app.cell
def _(engine, plt):
    sub_category_expenses = engine.execute("""
        SELECT 
            subcategory,
            SUM(amount) as total_expenses
        FROM fct_domestic_spending
        GROUP BY subcategory
        ORDER BY total_expenses DESC
    """).df()

    # Plot
    plt.figure(figsize=(8, 8))
    plt.pie(sub_category_expenses['total_expenses'], 
            labels=sub_category_expenses['subcategory'],
            autopct='%1.1f%%')
    plt.title('Expense Distribution by Category')
    plt.show()

    return


@app.cell
def _(mo):
    mo.md(r"""## Daily Expense Distribution""")
    return


@app.cell
def _(engine, plt, sns):
    daily_expenses = engine.execute("""
        SELECT 
            amount
        FROM fct_domestic_spending
        ORDER BY date
    """).df()

    # Plot
    plt.figure(figsize=(10, 6))
    sns.histplot(daily_expenses['amount'], bins=10, kde=True)
    plt.title('Distribution of Daily Expenses')
    plt.xlabel('Amount')
    plt.ylabel('Frequency')
    plt.show()
    return


@app.cell
def _(mo):
    mo.md(r"""## Cumulative Expenses Over Time""")
    return


@app.cell
def _(engine, plt, sns):
    cumulative_expenses = engine.execute("""
        SELECT 
            date,
            SUM(amount) OVER (ORDER BY date) as cumulative_expenses
        FROM fct_domestic_spending
        ORDER BY date
    """).df()

    # Plot
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=cumulative_expenses, x='date', y='cumulative_expenses')
    plt.title('Cumulative Expenses Over Time')
    plt.xlabel('Month')
    plt.ylabel('Cumulative Amount')
    plt.tight_layout()
    plt.show()

    return


@app.cell
def _(mo):
    mo.md(r"""## Uncategories expenses""")
    return


@app.cell
def _(engine, fct_domestic_spending, mo):
    _df = mo.sql(
        f"""
        SELECT
            *
        FROM
            fct_domestic_spending
        WHERE
            category = 'Other'
        order by
            amount desc,
            date desc
        limit
            50;
        """,
        engine=engine
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## Category Trends Over Time""")
    return


@app.cell
def _(engine, plt, sns):
    category_trends = engine.execute("""
        SELECT 
            strftime(date, '%Y-%m') as month,
            category,
            SUM(amount) as total_expenses
        FROM fct_domestic_spending
        GROUP BY month, category
        ORDER BY month, category
    """).df()

    # Pivot the data for heatmap
    heatmap_data = category_trends.pivot(index='category', columns='month', values='total_expenses')

    # Plot heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap='YlOrRd', annot=True, fmt='.0f', 
                linewidths=.5, cbar_kws={'label': 'Expense Amount'})
    plt.title('Monthly Expense Trends by Category')
    plt.xlabel('Month')
    plt.ylabel('Category')
    plt.tight_layout()
    plt.show()
    return


if __name__ == "__main__":
    app.run()
