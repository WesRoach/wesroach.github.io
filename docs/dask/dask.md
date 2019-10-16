# Dask Working Notes

## Rotate Long Column Wide - Multiple

```python
import pandas as pd
import dask.dataframe as dd
import numpy as np


def convert_dates_to_strings(df, date_columns: list, date_format) -> dd.DataFrame:
    for col in date_columns:
        df[col] = df[col].dt.strftime(date_format)
        df[col] = df[col].replace("01011800", "")
    return df
    

df = pd.DataFrame(
    {
        "bene_id": ["1", "1", "1", "1", "1"],
        "hdr_icn": ["1", "1", "2", "2", "2"],
        "rot1": ["A", "B", "C", " ", "E"],
        "rot2": ["X", "Y", "Z", " ", " "],
        "rot3": [
            pd.to_datetime("2018-01-01"),
            pd.to_datetime("2018-01-01"),
            pd.to_datetime("2018-01-01"),
            pd.to_datetime("2018-01-01"),
            pd.to_datetime("2018-01-01"),
        ],
    }
)
ddf = dd.from_pandas(df, 4)
ddf = convert_dates_to_strings(ddf, ["rot3"], "%m%d%Y")
ddf = ddf.set_index("bene_id").persist()


def agg_func(x):
    return pd.Series(
        dict(
            # 14.7 ms ± 287 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
            # rot1="%s" % ";".join(x["rot1"]),
            # rot2="%s" % ";".join(x["rot2"]),
            # rot3="%s" % ";".join(x["rot3"]),
            # 14.7 ms ± 493 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
            # rot1=f'{";".join(x["rot1"])}',
            # rot2=f'{";".join(x["rot2"])}',
            # rot3=f'{";".join(x["rot3"])}',
            # 14.8 ms ± 314 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
            rot1=";".join(x["rot1"]),
            rot2=";".join(x["rot2"]),
            rot3=";".join(x["rot3"]),
        )
    )

%%timeit
ddf.groupby(["bene_id", "hdr_icn"]).apply(
    agg_func, meta={"rot1": "str", "rot2": "str", "rot3": "str"}
).compute()
len(ddf.dask)
```
