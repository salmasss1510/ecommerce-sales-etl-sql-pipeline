from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, when


# --------------------------------------------------
# 1. Start Spark
# --------------------------------------------------

spark = (
    SparkSession.builder
    .appName("ECommerceETL")
    .master("local[*]")
    .getOrCreate()
)

print("Spark started successfully")


# --------------------------------------------------
# 2. Read raw CSV
# --------------------------------------------------

input_file = "data/online_retail.csv"

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(input_file)
)

print(f"Raw record count: {df.count()}")


# --------------------------------------------------
# 3. Clean column names
# --------------------------------------------------

df = df.select(
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country"
)


# --------------------------------------------------
# 4. Remove rows with missing important values
# --------------------------------------------------

df = df.dropna(
    subset=[
        "InvoiceNo",
        "StockCode",
        "Quantity",
        "UnitPrice"
    ]
)


# --------------------------------------------------
# 5. Remove invalid transactions
# --------------------------------------------------

df = df.filter(col("Quantity") > 0)
df = df.filter(col("UnitPrice") > 0)


# --------------------------------------------------
# 6. Clean text fields
# --------------------------------------------------

df = df.withColumn(
    "Description",
    trim(col("Description"))
)

df = df.withColumn(
    "Country",
    trim(col("Country"))
)


# --------------------------------------------------
# 7. Remove duplicate transactions
# --------------------------------------------------

df = df.dropDuplicates()


# --------------------------------------------------
# 8. Create revenue column
# --------------------------------------------------

df = df.withColumn(
    "Revenue",
    col("Quantity") * col("UnitPrice")
)


# --------------------------------------------------
# 9. Display results
# --------------------------------------------------

print(f"Cleaned record count: {df.count()}")

print("\nSchema:")
df.printSchema()

print("\nSample cleaned records:")
df.show(10, truncate=False)


# --------------------------------------------------
# 10. Save cleaned data
# --------------------------------------------------

output_path = "data/cleaned_retail"

(
    df.write
    .mode("overwrite")
    .option("header", True)
    .csv(output_path)
)

print(f"\nCleaned data saved to: {output_path}")


# --------------------------------------------------
# 11. Stop Spark
# --------------------------------------------------

spark.stop()

print("ETL transformation completed successfully!")