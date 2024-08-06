# Metadata

The central part of the catalog is the list of stations and their metadata which is displayed on the [station catalog page](station_catalog). The metadata for each station includes:
* Station name
* Station abbreviation
* State/region and country
* Latitude, longitude, and elevation (according to ISO 6709)
* Time period of operation
* Station owner and network (e.g., BSRN, SURFRAD)
* Link to the station or network website
* Data availability ("Freely", "Upon request", "Not available", or blank if unknown)
* Station tier (see [station requirements](station_requirements)).
* Instruments and components

## Time-period
The time period should identify for which years data is available, which is useful for several reasons. Knowing the time period allows for identifying which stations are still active and how long of a historical record of data is available.

A station that started operating in 2013 which does not have data for 2014 and 2017, but is still active would have a time period entry of: `2013&2015-2016&2018-`. For BSRN stations the time period should be identified based on the available data, which can be seen [here](https://dataportals.pangaea.de/bsrn/). In case it is unknown if a station is still in operation, a question mark is added at the end of the time period, e.g., `2012-?`.

## Instruments and components
Metadata concerning the instrumentation and which components are measured is highly useful when determining if a station is of interest for a particular study. The instrument column denotes whether irradiance is measured using traditional thermopile instruments or using special instruments (such as SPN1 or rotating shadowband pyranometers (RSR or RSI). In the components column, the measured components are denoted by one or more letters separated by semicolons. An example could be `G;B;D;UV;IR` (the order of components should be given as in the example).

## Latitude and longitude
The latitude and longitude of the station should be specified with at least four decimals. This guarantees an [accuracy](http://wiki.gis.com/wiki/index.php/Decimal_degrees) of +/- 5.6 m, which allows users to identify the location of the solar tracker/platform on the map.
