**Problem Statement:**
The Phonepe pulse Github repository contains a large amount of data related to various metrics and statistics. The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.

**Approach:**
**Data extraction**: Cloning the Github using scripting to fetch the data from the Phonepe pulse Github repository.
**Data transformation**: Using Python, we manipulate and pre-process the data from complex to simple format so that we can use the data to visualize.
**Data Export to MYSQL database:** We export the cleaned data to a MYSQL database using "mysql-connector-python" library and store the data.
****Data Import**: we import the data from MYSQL db using "mysql-connector-python" and store it under a dataframes for further use.
**Dashboard:** Using the Streamlit and Plotly libraries we create an interactive dashboard with menu option so that we can navihgate to different sections of our **visualization:** There are also filters to see specific data through visuals from dashboard

**Packages:**
streamlit
pandas
base64
mysql-connector-python
plotly-express
geopandas
streamlit-option-menu
matplotlib
