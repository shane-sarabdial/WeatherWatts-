# Predicting Energy Demand

## Authors

Edward Oh | Islam Orabi | Shane Sarabdial

## Table of Contents

- [Introduction](#introduction)
- [Data Sources](#Data-Sources)
- [Data Procesing and ETL](#Data-Processing-and-ETL)
- [Visualizations](#Visualizations)
- Results
- Resources??? same as data sources???

## Introduction

dgfgdf

-
- intro
-
- motivation
- What is an ISO -map
- What is XLE
- Data sources
- explain ml model -4
- explain etl process - 3
- EDA process - 8
- dash - 2

## Data Sources
- [EIA](https://www.eia.gov/opendata/)
- [Weather](https://www.visualcrossing.com/)
- [XLE](https://finance.yahoo.com/quote/XLE/history?p=XLE)
- [Holidays](https://www.timeanddate.com/holidays/us/)

## Data Processing and ETL
Static data was pulled from 4 different sources utilizing API, CSV downloads and webscraping. That data was then cleaned and saved in our azure cloud storage container. We used that clean data to do exploratory data analysis and create our machine learning model with [LightGBM](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMRegressor.html). Every 24 hours, live weather data was pulled using an API to be cleaned, produced and consumed in databricks and Kafka. This process is automated using Azure Data Factory. The consumed data is stored in a SQL database to be inputted in our machine learning model. Visualizations are created using Dash and publicly displayed on our [website](https://weatherwatts.onrender.com/).

![pipeline](/Images/FinalPipeline.png)


## Visualizations
![Texas](/Images/Texas.png)
-Info ABout Texas
![Florida](/Images/Florida.png)
-Infor about Florida
![California](/Images/california.png)
-Info about california


###### dfddf
