import camelot
import pandas as pd
import os
import sys
import glob
import duckdb


def parse_regalia_gold(file_path, pdf_pass):
    print(f"Processing {file_path}")
    # Process - E-Statement <month> <year>
    file_name = os.path.basename(file_path)
    timestamp = "-".join(file_name.split(".pdf")[0].split(" ")[1:])
    csv_name_domestic = f"regalia-domestic-{timestamp}"
    csv_name_international = f"regalia-international-{timestamp}"

    out_path = "data/csv"

    tables = camelot.read_pdf(file_path, password=pdf_pass, pages="all", flavor="stream")

    domestic_spending = []
    for idx in range(len(tables)):
        table = tables[idx].df
        if table[1][0] == "Domestic Transactions":
            domestic_spending.append(table)

    pd.concat(domestic_spending).to_csv(f"{out_path}/{csv_name_domestic}.csv", header=False)

    # TODO: Add international travel

def main():

    pdf_pass = os.getenv("PDF_PASS")

    if len(sys.argv) < 2:
        print("Usage: parse_regalia_statement <glob>")
        sys.exit(1)

    prefix = sys.argv[1]

    for filename in glob.glob(f'{prefix}*'):
        parse_regalia_gold(filename, pdf_pass)


main()
