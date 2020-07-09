# OpenDataCampusIF

Mini-project on public transport infrastructure.
Created during Open Data Campus Ivano-Frankivsk on 2-5 July, 2020 (http://campus.texty.org.ua/).

The project was aimed to collect, analyze and visualize data about public transport in Ivano-Frankivsk city.
and provide recommendations for public and municipal authorities based on the analyzed data.

Code samples from this repository were designed to 
* parse logs from city.dozor.tech website which does not have public API
  (see https://github.com/MykolaKlishch/OpenDataCampusIF/tree/master/dozor_logs);
* retrieve useful data 
  (coordinates and speed of each bus and trolleybus every ~10 seconds + bus stop coordinates);
* transform the data and save them in CSV and JSON files.

Generated CSV and JSON files were fed to Kepler to produce geospatial interactive visualisations 
(check https://github.com/MykolaKlshch/OpenDataCampusIF/tree/master/kepler for visualisations)
