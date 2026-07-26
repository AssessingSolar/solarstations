



```{marimo} python
import marimo as mo
import pandas as pd
# Load stations
solarstations = pd.read_csv('../solarstations.csv', dtype={'Tier': str}).fillna('')

# df is a Pandas or Polars dataframe
table = mo.ui.table(
    data=solarstations,
    # use pagination when your table has many rows
    pagination=True,
    label="Dataframe",
)
```

```{marimo} python
table
```
