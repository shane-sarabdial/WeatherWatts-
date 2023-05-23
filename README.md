# Predicting Energy Demand

## Authors

Edward Oh | Islam Orabi | Shane Sarabdial

## Table of Contents

- [Introduction](#introduction)
- [Project Management Plan](#project-management-plan)
- [Data Sources](#data-sources)
- [Data Procesing and ETL](#data-processing-and-etl)
- [Visualizations](#visualizations)
- [Website Features](#website-features)
- [Machine Learning](#machine-learning)
- [Results](#results)
- [Resources](#references)

## Introduction
- intro


- motivation


- What is an ISO -map


- What is XLE


- dash - 2

## Project Management Plan
![pmp](/Images/Trello.png)

## Data Sources
- [EIA](https://www.eia.gov/opendata/)
- [Weather](https://www.visualcrossing.com/)
- [XLE](https://finance.yahoo.com/quote/XLE/history?p=XLE)
- [Holidays](https://www.timeanddate.com/holidays/us/)

## Data Processing and ETL
Static data was pulled from 4 different sources utilizing API, CSV downloads and webscraping. That data was then cleaned and saved in our azure cloud storage container. We used that clean data to do exploratory data analysis and create our machine learning model with [LightGBM](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMRegressor.html). Every 24 hours, live weather data was pulled using an API to be cleaned, produced and consumed in databricks and Kafka. This process is automated using Azure Data Factory. The consumed data is stored in a SQL database to be inputted in our machine learning model. Visualizations are created using Dash and publicly displayed on our [website](https://weatherwatts.onrender.com/).

![pipeline](/Images/FinalPipeline.png)


## Visualizations
![Conditions](/Images/EDA/conditions_barchart.png)

![LineChart](/Images/EDA/energydemand_linechart.png)

![Subplots](/Images/EDA/subplots.png)

![ScatterPlot](/Images/EDA/demand_scatterplot.png)

![ScatterPlot2](/Images/EDA/generation_scatterplot.png)

![Texas](/Images/Texas.png)

![Florida](/Images/Florida.png)

![California](/Images/california.png)

## Website Features

![range of demand](/Images/GIFS/range%20of%20demand.gif)

![week select](/Images/GIFS/week%20select.gif)

![zoom in data](/Images/GIFS/zoom%20main.gif)

## Machine Learning

- [LightGBM](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMRegressor.html)

## Results


## References

- [2021 Texas Winter Storm](https://environmentamerica.org/texas/center/articles/the-texas-freeze-timeline-of-events/)
- [2017 Florida hurricane Irma](https://www.weather.gov/mfl/hurricaneirma)
- [2022 California Heatwave](http://www.caiso.com/Documents/california-iso-posts-analysis-of-september-heat-wave.pdf)
