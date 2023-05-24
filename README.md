# Predicting Energy Demand

---

## Authors

---

Edward Oh | Islam Orabi | Shane Sarabdial

## Table of Contents

---

- [Introduction](#introduction)
- [Project Management Plan](#project-management-plan)
- [Data Sources](#data-sources)
- [Data Procesing and ETL](#data-processing-and-etl)
- [Visualizations](#visualizations)
- [Machine Learning](#machine-learning)
- [Website Features and Dashboard](#website-features)
- [Results](#results)
- [Resources](#references)

## Introduction

---

The demand for energy and its price has surged in the last few years due to political, environmental and geological factors. Today we aim to identify the key features that can impact energy demand in a select few states. Our focus are on the states of California, New York, Texas, and Florida. Read our technical report to get the full details of our project.

## Project Management Plan

---

![pmp](/Images/Trello.png)

## Data Sources

---

- [EIA](https://www.eia.gov/opendata/)
- [Weather](https://www.visualcrossing.com/)
- [XLE](https://finance.yahoo.com/quote/XLE/history?p=XLE)
- [Holidays](https://www.timeanddate.com/holidays/us/)

## Data Processing and ETL

---

Static data was pulled from 4 different sources utilizing API, CSV downloads and web scraping. That data was then cleaned and saved in our azure cloud storage container. We used that clean data to do exploratory data analysis and create our machine learning model with [LightGBM](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMRegressor.html). Every 24 hours, live weather data is pulled using an API to be cleaned, produced, and consumed in databricks and Kafka. This process is automated using Azure Data Factory. The consumed data is stored in a SQL database to be inputted in our machine learning model. Visualizations are created using Dash and publicly displayed on our [website](https://weatherwatts.onrender.com/).

![pipeline](/Images/FinalPipeline.png)

## Visualizations

---

In this graph we see Texas has the highest energy demand of all states. New York has almost the same energy demand no matter the weather conditions. In Los Angeles, when the weather condition is overcast the energy demand is highest in California and lowest when the weather is rainy and partially cloudy. As for Tampa, when the weather is rainy and partially cloudy, the energy demand in Florida is highest and when the weather is overcast the energy demand is lowest.

![Conditions](/Images/EDA/conditions_barchart.png)

The scatter plot displays the hourly average energy demand in megawatt hours against the population in Texas, California, Florida and New York. The pie chart represents the percentage population in each state with California having the highest population, followed by Texas, Florida and New York. On the scatter plot, despite California having the highest population, the state’s energy demand is second lowest. Texas on the other hand, has the highest energy demand while being the second most populous state.

![Subplots](/Images/EDA/subplots.png)

We also investigated the state area and demand and found that there was a weak correlation between the two.

![ScatterPlot2](/Images/EDA/generation_scatterplot.png)

We looked at the energy demand before, after and during a natural disaster. We looked at hurricane Irma, the 2021 Texas winter storm, and heatwaves in Los Angeles in 2022. The image below shows that for Texas, power demand peaked at 70K megawatt hours and continued to decline in the coming days. Texas is on a isloated power grid and was unable to borrow power from other states.

![Texas](/Images/Texas.png)

To see all our visuals please read the technical report.

## Machine Learning

---

We tried several ML models including Histogram Gradient Boosting Regressor, XGBoost and Random Forest, but ultimately settled on [LightGBM](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMRegressor.html). LGBM gave us better accuracy and faster training times.
For our model we did feature engineering and created the following features

- 3 day lag in energy demand
- 3- , 30-, and 60-day lag in XLE. XLE is a energy index that tracks energy companies. We used this representaion of energy prices.
- Foracsted tempertures 1 day ahead.
- Encoded 25 holidays
- Created a hour, day, month, day of week, quarter, and day of year feature,
- Created a weekend feature.

The model was cross validated over 3 time periods and was scored using both RMSE and MAE.

![time_series_split](/Images/ts_split.png)

## Website Features and Dashboard

---

Our website was created using dash and deployed on [render](https://dashboard.render.com/).

![range of demand](/Images/GIFS/range%20of%20demand.gif)

![week select](/Images/GIFS/week%20select.gif)

![zoom in data](/Images/GIFS/zoom%20main.gif)

## Results

---

| State| RMSE| MAE|
| --- | ---  | ---  |
| CA  | 1721 | 1220 |
| FL  | 2029 | 1464 |
| NY  | 872  | 638  | 
| TX  | 3484 | 2606 |


## References

---

- [2021 Texas Winter Storm](https://environmentamerica.org/texas/center/articles/the-texas-freeze-timeline-of-events/)
- [2017 Florida hurricane Irma](https://www.weather.gov/mfl/hurricaneirma)
- [2022 California Heatwave](http://www.caiso.com/Documents/california-iso-posts-analysis-of-september-heat-wave.pdf)
- [Dash for Python Documentation](https://dash.plotly.com/dash-enterprise)
- [Charming Data - YouTube](https://www.youtube.com/@CharmingData)
- [Plotly Python Graphing Library](https://plotly.com/python/)
- [Census Population Data](https://statics.teams.cdn.office.net/evergreen-assets/safelinks/1/atp-safelinks.html)
- [50 States Ranked By Size, In Square Miles](https://thefactfile.org/50-states-area/)
- [U.S. Energy Information Administration Energy Source](https://www.eia.gov/state/?sid=US)
- [U.S. Energy Information Administration - EIA Hurriacne Irma](https://www.eia.gov/todayinenergy/detail.php?id=32992)
- [2021 Texas power crisis - Wikipedia](https://en.wikipedia.org/wiki/2021_Texas_power_crisis)
- [pandas 2.0.1 documentation](https://pandas.pydata.org/docs/index.html)
- [scikit-learn 1.2.2 documentation](https://scikit-learn.org/stable/index.html)

