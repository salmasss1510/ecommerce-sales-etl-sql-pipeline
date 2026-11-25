import csv
from openpyxl import load_workbook

input_file = "data/Online Retail.xlsx"
output_file = "data/online_retail.csv"

print("Reading Excel dataset...")

# Read Excel file in read-only mode
workbook = load_workbook(input_file, read_only=True)
sheet = workbook.active

# Get the header
rows = sheet.iter_rows(values_only=True)
header = next(rows)

print("Columns:")
print(header)

# Create CSV file
with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)

    # Write header
    writer.writerow(header)

    # Write all rows
    row_count = 0

    for row in rows:
        writer.writerow(row)
        row_count += 1

print(f"Total records converted: {row_count}")
print(f"CSV created successfully: {output_file}")

workbook.close()