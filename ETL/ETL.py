# Databricks notebook source
# DBTITLE 1,Reading in necesary file to ETL -> Kafka Produce
df = spark.read.parquet('/mnt/weatherwatts/EIApartition', header = True, inferSchema=True) #edit the mountpoint directory to read in the necessary file

# COMMAND ----------

display(df)

# COMMAND ----------

### ETL STEPS

# COMMAND ----------

df.columns

# COMMAND ----------

from pyspark.sql.functions import col
from pyspark.sql import SparkSession
from pyspark.sql.functions import isnull

# COMMAND ----------

df.printSchema()

# COMMAND ----------

from pyspark.sql.functions import year, month, dayofweek, hour, quarter, dayofyear

# COMMAND ----------

def create_features(dfs):
    dfs = dfs.withColumn("year", year("period"))
    dfs = dfs.withColumn("month", month("period"))
    dfs = dfs.withColumn("days", dayofweek("period"))
    dfs = dfs.withColumn("hour", hour("period"))
    dfs = dfs.withColumn("quarter", quarter("period"))
    dfs = dfs.withColumn("dayofyear", dayofyear("period"))
    return dfs

# COMMAND ----------

df = create_features(df)

# COMMAND ----------

# DBTITLE 1,parsing the timestamp
df.show()

# COMMAND ----------

df = df.drop('type')

# COMMAND ----------

df_demand = df.filter(df['type-name'] == 'Demand')

# COMMAND ----------

df_generation = df.filter(df['type-name'] == 'Net generation')

# COMMAND ----------

# DBTITLE 1,Reading in weather CSV and storing to df2
df2 = spark.read.csv('/mnt/weatherwatts/weather.csv', header = True, inferSchema=True)

# COMMAND ----------

df2.printSchema()

# df.set_index('period') 

# COMMAND ----------

display(df2.summary())

# COMMAND ----------

# DBTITLE 1,Dropping unnecessary columns
df2 = df2.drop('windgust')
df2 = df2.drop('severerisk')
df2 = df2.drop('preciptype')
df2 = df2.drop('solarenergy')
df2 = df2.drop('stations')

# COMMAND ----------

df2 = df2.withColumnRenamed('datetime', 'period')

# COMMAND ----------

df2 = create_features(df2)

# COMMAND ----------

display(df2)

# COMMAND ----------

df2 = df2.repartition(1)
df2.write.mode("overwrite").parquet('/mnt/weatherwatts/weather')

# COMMAND ----------

df_generation = df_generation.repartition(1)
df_generation.write.mode("overwrite").parquet('/mnt/weatherwatts/energy_generation')

# COMMAND ----------

df_demand = df_demand.repartition(1)
df_demand.write.mode("overwrite").parquet('/mnt/weatherwatts/energy_demand')

# COMMAND ----------

