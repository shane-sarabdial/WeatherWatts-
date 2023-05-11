# Databricks notebook source
# MAGIC %run "/Shared/WeatherWatts/config/api keys"

# COMMAND ----------

import requests
import pandas as pd

# COMMAND ----------

locations =[ "CISO", "ERCO","NYIS","FLA"]


# COMMAND ----------

# DBTITLE 1,Function to convert json to pandas df
def json_to_dateframe(response):
    return pd.DataFrame(response.json()['response']['data'][1:], columns= response.json()['response']['data'][0])

# COMMAND ----------

# DBTITLE 1,RUN ONCE to consume API
from time import sleep
df_final = pd.DataFrame()
for loc in locations:
    for x in range(0,145_000,5000):
        try:
            url = f'https://api.eia.gov/v2/electricity/rto/region-data/data/?api_key={key}&frequency=hourly&data[0]=value&facets[type][]=D&facets[type][]=NG&facets[respondent][]={loc}&sort[0][column]=period&sort[0][direction]=asc&offset={x}&length=5000'
            response = requests.get(url)
            df = json_to_dateframe(response)
            df_final = pd.concat([df_final,df])
            print(response)
            if x%50000 == 0:
                sleep(45)
        except:
            print('error')

# COMMAND ----------

# MAGIC %md
# MAGIC sparkDF=spark.createDataFrame(pandasDF) 

# COMMAND ----------

df = spark.createDataFrame(df_final)

# COMMAND ----------

display(df)

# COMMAND ----------

display(dbutils.fs.mounts())

# COMMAND ----------

# DBTITLE 1,Writing to CSV/parquet file in our shared storage container
df = df.repartition(1)
df.write.mode("overwrite").parquet('/mnt/weatherwatts/EIApartition') 

# COMMAND ----------

