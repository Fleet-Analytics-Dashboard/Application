# Fleetboard

This project was developed for the course "338025 Data Science Project - Optimizing Fleet Management" of [Prof. Dr. Jan Kirenz](mailto:kirenz@hdm-stuttgart.de?subject=[GitHub]Fleetboard) at the Stuttgart Media University. The dashboard was developed by [Lucie](https://github.com/lj025), [Tim](https://github.com/ts170), [Larisa](https://github.com/LarisaCiupe), [Jakob](https://github.com/jakobschaal), [Johannes](https://github.com/johannesstroebele91).

## Project Goal
This dashboard supports fleet managers and decision makers to gain insights into their automotive fleets and optimize them. The data foundation for this the [NREL Fleet DNA project Truck Platooning Data](https://data.world/smartcolumbusos/636302d3-1197-4d38-9abf-9ffef44d4570) and simulated data by [Tim](https://github.com/ts170).
![image](https://user-images.githubusercontent.com/33202527/88454271-a9e06000-ce6e-11ea-82e7-86f10d01be60.png)

It consists of three pages for satisfying the need of different target groups:

* Home view: especially controllers and financial officer can quickly gain insights into the most important key metrics and make high level decisions (e.g. Revenue, Costs, Capacity Overview)
* Downtimes: this page enables fleet managers to easily monitor their fleet and respond to various challenges fast and confidently
* Vehicle overview: if detailed information about certain vehicles or their position in real time on a map is neded, fleet managers can view this information on this page 

## Wiki page
_The wiki has the following sub pages:_

1. [Home](https://github.com/Fleet-Analytics-Dashboard/Application/wiki)
2. [Goals](https://github.com/Fleet-Analytics-Dashboard/Application/wiki/Goals)
3. [Solution Approach](https://github.com/Fleet-Analytics-Dashboard/Application/wiki/Solution-Approach)
4. [User Research](https://github.com/Fleet-Analytics-Dashboard/Application/wiki/User-Research)
5. [Design Concept](https://github.com/Fleet-Analytics-Dashboard/Application/wiki/Design-Concept)
6. [Data Foundation](https://github.com/Fleet-Analytics-Dashboard/Application/wiki/Data-Foundation)
7. [Technology stack](https://github.com/Fleet-Analytics-Dashboard/Application/wiki/Technology-stack)
8. [Data Science](https://github.com/Fleet-Analytics-Dashboard/Application/wiki/Data-Science)
9. [Dashboard Explanation](https://github.com/Fleet-Analytics-Dashboard/Application/wiki/Dashboard-Explanation)
10. [Lessons Learned](https://github.com/Fleet-Analytics-Dashboard/Application/wiki/Lessons-Learned)
11. [Potential Improvements](https://github.com/Fleet-Analytics-Dashboard/Application/wiki/Potential-Improvements)

## Repository Structure
_The files in this repository have the following purpose:_
* .gitignore: enables to ignore files that should not be pushed like database config file
* apps: all of the dashboard views can be found here
* assets: logo and stylesheet
* csv_data_files: data foundation as CSV files (as a fallback in case of database issues)
* data_preparation: Python scripts for preparing the raw [NREL Fleet DNA project Truck Platooning](https://data.world/smartcolumbusos/636302d3-1197-4d38-9abf-9ffef44d4570) and simulated data
* hidden: needs to be created with a database.config file inside to connect to the project's PostgreSQL database (ask [Johannes](https://github.com/johannesstroebele91) for database connection information)
* __init__.py: required to make Python treat the directories as containing packages 
* app.yaml: contains the definition of the Python runtime, the entrypoint Gunicorn, and the database connection (need to be specified in the database.config as explained above
* data_preparation_run.py: Python script for running the data preparation
* database_connection.py: Python script for connecting to the database
* main.py: entrypoint of the application
* requirements.txt: consists of all dependencies necessary for running the application

## Software Architecture
_This is the current software architecture. More information can be found on the([technology stack wiki page](https://github.com/Fleet-Analytics-Dashboard/Application/wiki/Technology-stack):_ 
![image](https://user-images.githubusercontent.com/33202527/88454999-cf6f6880-ce72-11ea-9240-909a62367152.png)

## Lessons Learned
_Are more detailed list can be found [on the lessons learned wiki page](https://github.com/Fleet-Analytics-Dashboard/Application/wiki/Lessons-Learned)_

* Creation of business value from data insights (maintenance prediction)
* Predictions with XGBoost and data transformation with pandas and NumPy
* Deployment of Dash app via Gunicorn HTTP server on Google Cloud App Engine
* Working with different python libraries (e.g. Dash, Plotly. pandas, Numpy)
* Creating a dashboard with user-centric data visualization (different views for different target groups)
* Communication is key (GitHub tasks, video calls, documentation, comments)

## Contact
* [Lucie](https://github.com/lj025)
* [Tim](https://github.com/ts170)
* [Larisa](https://github.com/LarisaCiupe)
* [Jakob](https://github.com/jakobschaal)
* [Johannes](https://github.com/johannesstroebele91)

## License

MIT License - Copyright 2020 ©
