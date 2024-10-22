# Metadata

The central part of the catalog is the list of stations and their metadata which is displayed on the SolarStations.Org [station catalog page](station_catalog). The metadata for each station includes:
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
Metadata concerning the instrumentation and which components are measured is highly useful when determining if a station is of interest for a particular study. The instrumentation column denotes the type of instruments deployed at a site, from which the measured components can be derived. The possible components are:
* Global horizontal irradiance (GHI)
* Direct normal irradiance (DNI)
* Direct horizontal irradiance (DHI)
* Ultraviolet irradiance (UV)
* Longwave downwelling irradiance (LWD)
* Photosynthetic active radiation (PAR)

The following instrument options are available:
| Instrumentation | Description | Components measured |
|---|---|---|
| `G` | Unshaded thermopile pyranometer | GHI |
| `B` | Thermopile pyrheliometer mounted on a solar tracker | DNI |
| `D` | Shaded thermopile pyranometer mounted on a solar tracker | DHI |
| `Ds` | Thermopile pyranometer shaded by a shadowring | DHI |
| `IR` | Pyrgeometer| LWD |
| `UV/UVA/UVB` | UV radiometer | UV |
| `PAR` | Radiometer sensitive to photoactive radiation (PAR) | PAR |
| `SPN1` | Multi-sensor pyranometer from Delta-T | GHI/DNI/DHI |
| `RSR/RSI/RSP` | Rotating shadowband radiometer/pyranometer | GHI/DNI/DHI |

## Latitude and longitude
The latitude and longitude of the station should be specified with at least four decimals. This guarantees an [accuracy](http://wiki.gis.com/wiki/index.php/Decimal_degrees) of +/- 5.6 m, which allows users to identify the location of the solar tracker/platform on the map.
