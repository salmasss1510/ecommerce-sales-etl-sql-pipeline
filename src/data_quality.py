import mysql.connector


# --------------------------------------------------
# Connect to MySQL
# --------------------------------------------------

connection = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="root",
    database="ecommerce_dw"
)

cursor = connection.cursor()

print("=" * 60)
print("DATA QUALITY CHECKS")
print("=" * 60)


# --------------------------------------------------
# 1. Fact table record count
# --------------------------------------------------

cursor.execute("""
    SELECT COUNT(*)
    FROM fact_sales
""")

total_sales = cursor.fetchone()[0]

print(f"\n1. Total sales records: {total_sales}")

if total_sales > 0:
    print("   PASS")
else:
    print("   FAIL")


# --------------------------------------------------
# 2. Check negative quantity
# --------------------------------------------------

cursor.execute("""
    SELECT COUNT(*)
    FROM fact_sales
    WHERE quantity <= 0
""")

invalid_quantity = cursor.fetchone()[0]

print(f"\n2. Invalid quantities: {invalid_quantity}")

if invalid_quantity == 0:
    print("   PASS")
else:
    print("   FAIL")


# --------------------------------------------------
# 3. Check invalid prices
# --------------------------------------------------

cursor.execute("""
    SELECT COUNT(*)
    FROM fact_sales
    WHERE unit_price <= 0
""")

invalid_price = cursor.fetchone()[0]

print(f"\n3. Invalid unit prices: {invalid_price}")

if invalid_price == 0:
    print("   PASS")
else:
    print("   FAIL")


# --------------------------------------------------
# 4. Check invalid revenue
# --------------------------------------------------

cursor.execute("""
    SELECT COUNT(*)
    FROM fact_sales
    WHERE revenue <= 0
""")

invalid_revenue = cursor.fetchone()[0]

print(f"\n4. Invalid revenue values: {invalid_revenue}")

if invalid_revenue == 0:
    print("   PASS")
else:
    print("   FAIL")


# --------------------------------------------------
# 5. Check missing customer IDs
# --------------------------------------------------

cursor.execute("""
    SELECT COUNT(*)
    FROM fact_sales
    WHERE customer_id IS NULL
       OR customer_id = ''
""")

missing_customers = cursor.fetchone()[0]

print(f"\n5. Missing customer IDs: {missing_customers}")

if missing_customers == 0:
    print("   PASS")
else:
    print("   WARNING")


# --------------------------------------------------
# 6. Check orphan customer records
# --------------------------------------------------

cursor.execute("""
    SELECT COUNT(*)
    FROM fact_sales f
    LEFT JOIN dim_customer c
        ON f.customer_id = c.customer_id
    WHERE c.customer_id IS NULL
""")

orphan_customers = cursor.fetchone()[0]

print(f"\n6. Orphan customer records: {orphan_customers}")

if orphan_customers == 0:
    print("   PASS")
else:
    print("   FAIL")


# --------------------------------------------------
# 7. Check orphan products
# --------------------------------------------------

cursor.execute("""
    SELECT COUNT(*)
    FROM fact_sales f
    LEFT JOIN dim_product p
        ON f.stock_code = p.stock_code
    WHERE p.stock_code IS NULL
""")

orphan_products = cursor.fetchone()[0]

print(f"\n7. Orphan product records: {orphan_products}")

if orphan_products == 0:
    print("   PASS")
else:
    print("   FAIL")


# --------------------------------------------------
# 8. Check revenue calculation
# --------------------------------------------------

cursor.execute("""
    SELECT COUNT(*)
    FROM fact_sales
    WHERE ABS(revenue - (quantity * unit_price)) > 0.01
""")

incorrect_revenue = cursor.fetchone()[0]

print(f"\n8. Incorrect revenue calculations: {incorrect_revenue}")

if incorrect_revenue == 0:
    print("   PASS")
else:
    print("   FAIL")


# --------------------------------------------------
# Summary
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATA QUALITY CHECKS COMPLETED")
print("=" * 60)


cursor.close()
connection.close()