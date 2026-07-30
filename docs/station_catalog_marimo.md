```{marimo} python
import marimo as mo
import pandas as pd
```


```{marimo} python
main_url = "https://raw.githubusercontent.com/AssessingSolar/solarstations/refs/heads/main/solarstations.csv"
esmap_url = "https://raw.githubusercontent.com/AssessingSolar/solarstations/refs/heads/main/esmap_stations.csv"

main_stations = pd.read_csv(main_ur, dtype={'Tier': str}).fillna('')
esmap_stations = pd.read_csv(esmap_url, dtype={'Tier': str}).fillna('')
stations = pd.concat([main_stations, esmap_stations], axis='rows', ignore_index=True)

table = mo.ui.table(
    stations,
    pagination=True,
    freeze_columns_left=["Station name"],
    hidden_columns=["URL],
)
```

```{marimo} python
table
```