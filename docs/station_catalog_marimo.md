
```{marimo} python
import marimo as mo

slider = mo.ui.slider(start=1, stop=10, label="islands")
slider
```

```{marimo} python
mo.md(f"The slider is set to **{slider.value}**.")
```

```{marimo} python
from pathlib import Path

path = Path.cwd()
mo.md(str(path))
```

```{marimo} python
files = [str(f) for f in path.iterdir() if f.is_file()]
mo.ui.table(files)
```
