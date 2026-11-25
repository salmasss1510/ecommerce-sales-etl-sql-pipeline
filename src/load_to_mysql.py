import mysql.connector
import csv
import glob
from datetime import datetime


# --------------------------------------------------
# 1. Connect to MySQL
# --------------------------------------------------

connection = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="root",
    database="ecommerce_dw"
)

cursor = connection.cursor()

print("Connected to MySQL successfully!")


# --------------------------------------------------
# 2. Find ALL Spark CSV files
# --------------------------------------------------

files = sorted(
    glob.glob("data/cleaned_retail/part-*.csv")
)

if not files:
    raise FileNotFoundError("No cleaned CSV files found!")

print(f"Found {len(files)} cleaned CSV files")


# --------------------------------------------------
# 3. Prepare data containers
# --------------------------------------------------

customers = {}
products = {}
dates = {}
sales = []


# --------------------------------------------------
# 4. Read ALL cleaned CSV files
# --------------------------------------------------

for input_file in files:

    print(f"Reading: {input_file}")

    with open(input_file, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            customer_id = row["CustomerID"].strip()
            stock_code = row["StockCode"].strip()
            description = row["Description"].strip()
            country = row["Country"].strip()

            invoice_no = row["InvoiceNo"].strip()

            quantity = int(row["Quantity"])
            unit_price = float(row["UnitPrice"])
            revenue = float(row["Revenue"])


            # ------------------------------------------
            # Parse InvoiceDate
            # ------------------------------------------

            invoice_date = datetime.fromisoformat(
                row["InvoiceDate"].strip().replace("Z", "+00:00")
            )

            date_key = invoice_date.date()


            # ------------------------------------------
            # Customer dimension
            # ------------------------------------------

            if customer_id:

                customers[customer_id] = (
                    customer_id,
                    country
                )


            # ------------------------------------------
            # Product dimension
            # ------------------------------------------

            if stock_code:

                products[stock_code] = (
                    stock_code,
                    description
                )


            # ------------------------------------------
            # Date dimension
            # ------------------------------------------

            dates[date_key] = (
                date_key,
                date_key.year,
                date_key.month,
                date_key.day
            )


            # ------------------------------------------
            # Fact table
            # ------------------------------------------

            if customer_id:

                sales.append(
                    (
                        invoice_no,
                        stock_code,
                        customer_id,
                        date_key,
                        quantity,
                        unit_price,
                        revenue
                    )
                )


# --------------------------------------------------
# 5. Insert customers
# --------------------------------------------------

cursor.executemany(
    """
    INSERT IGNORE INTO dim_customer
    (customer_id, country)
    VALUES (%s, %s)
    """,
    list(customers.values())
)

print(f"Customers loaded: {len(customers)}")


# --------------------------------------------------
# 6. Insert products
# --------------------------------------------------

cursor.executemany(
    """
    INSERT IGNORE INTO dim_product
    (stock_code, description)
    VALUES (%s, %s)
    """,
    list(products.values())
)

print(f"Products loaded: {len(products)}")


# --------------------------------------------------
# 7. Insert dates
# --------------------------------------------------

cursor.executemany(
    """
    INSERT IGNORE INTO dim_date
    (date_key, year, month, day)
    VALUES (%s, %s, %s, %s)
    """,
    list(dates.values())
)

print(f"Dates loaded: {len(dates)}")


# --------------------------------------------------
# 8. Insert sales
# --------------------------------------------------

cursor.executemany(
    """
    INSERT INTO fact_sales
    (
        invoice_no,
        stock_code,
        customer_id,
        date_key,
        quantity,
        unit_price,
        revenue
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """,
    sales
)

print(f"Sales loaded: {len(sales)}")


# --------------------------------------------------
# 9. Commit changes
# --------------------------------------------------

connection.commit()

print("\nData loading completed successfully!")


# --------------------------------------------------
# 10. Close connection
# --------------------------------------------------

cursor.close()
connection.close()

print("MySQL connection closed.")