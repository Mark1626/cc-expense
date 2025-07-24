import camelot
import pandas as pd
import os
import sys
import glob
import duckdb


def parse_regalia_gold(file_path, pdf_pass):
    db = duckdb.connect("data/db/expense.db")

    print(f"Processing {file_path}")
    file_name = os.path.basename(file_path)
    timestamp = file_name.split(".PDF")[0].split("_")[1]
    csv_name_domestic = f"regalia-domestic-{timestamp}"
    csv_name_international = f"regalia-international-{timestamp}"

    out_path = "data/csv"

    tables = camelot.read_pdf(file_path, password=pdf_pass, pages="all", flavor="stream")
    
    # Domestic
    domestic_table_part_1 = tables[0].df
    domestic_table_part_2 = tables[1].df

    pd.concat([domestic_table_part_1, domestic_table_part_2]).to_csv(f"{out_path}/{csv_name_domestic}.csv", header=False)

    # International
    int_table = tables[2].df
    int_table.to_csv(f"{out_path}/{csv_name_international}.csv")

    # timestamp = timestamp.replace("-", "_")
    # db.sql(f"""
    # CREATE TABLE raw_data_regalia_domestic_{timestamp} AS 
    # SELECT * FROM read_csv('{out_path}/{csv_name}-domestic.csv', all_varchar=true)
    # """)

    # db.sql(f"""
    # CREATE TABLE raw_data_regalia_international_{timestamp} AS 
    # SELECT * FROM read_csv('{out_path}/{csv_name}-international.csv', all_varchar=true)
    # """)


def main():

    pdf_pass = os.getenv("PDF_PASS")

    if len(sys.argv) < 2:
        print("Usage: parse_regalia_statement <glob>")
        sys.exit(1)

    prefix = sys.argv[1]

    for filename in glob.glob(f'{prefix}*'):
        # print(filename)
        parse_regalia_gold(filename, pdf_pass)


main()
