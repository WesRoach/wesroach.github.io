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


ddf.groupby(["bene_id", "hdr_icn"]).apply(
    agg_func, meta={"rot1": "str", "rot2": "str", "rot3": "str"}
).compute()
```

We can condense some of this code down by passing a list of columns to agg_func.

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


def agg_func(x, cols):
    return pd.Series({col: ";".join(x[col]) for col in cols})


ddf.groupby(["bene_id", "hdr_icn"]).apply(agg_func, ["rot1", "rot2", "rot3"]).compute()
```

We can further reduce runtime by providing agg_func with the expected "meta" output from .apply(...)

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


def agg_func(x, cols):
    return pd.Series({col: ";".join(x[col]) for col in cols})


# On a subset of data, pass the groupby object to dask.dataframe.utils.make_meta()
ddf_meta = dd.utils.make_meta(ddf.groupby(["bene_id", "hdr_icn"]).apply(agg_func, ["rot1", "rot2", "rot3"]))
# You can view what you'll need to use as the meta object by accessing ddf_meta & ddf_meta.index
>> ddf_meta
Empty DataFrame
Columns: [rot1, rot2, rot3]
Index: []

>> ddf_meta.index
MultiIndex(levels=[['a', 'b'], ['foo']],
           codes=[[], []],
           names=['bene_id', 'hdr_icn'])

# The ddf_meta object obviously wont be available @ runtime - we use the output to manually define
# the object's properties
           
typed_ddf_meta = pd.DataFrame(
    columns=["rot1", "rot2", "rot3"],
    index=pd.MultiIndex(
        levels=[["a", "b"], ["foo"]], codes=[[], []], names=["bene_id", "hdr_icn"]
    ),
)
typed_ddf_meta = ddf_meta.astype(dtype={"rot1": "str", "rot2": "str", "rot3": "str"})

# note that the output of typed_ddf_meta and ddf_meta are equivalent

# you can now pass typed_ddf_meta as the meta object to .apply() - you should notice a marginal speedup
ddf.groupby(["bene_id", "hdr_icn"]).apply(agg_func, ["rot1", "rot2", "rot3"], meta=typed_ddf_meta).compute()
```

It wouldn't make sense to run the .groupby() @ runtime, every time, to generate the meta_ddf information, so we'll define it by hand below:

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


def agg_func(x, cols):
    return pd.Series({col: ";".join(x[col]) for col in cols})


# Create ddf_meta object representing expected output from .apply()
ddf_meta = pd.DataFrame(
    columns=["rot1", "rot2", "rot3"],
    index=pd.MultiIndex(
        levels=[["a", "b"], ["foo"]], codes=[[], []], names=["bene_id", "hdr_icn"]
    ),
)
ddf_meta = ddf_meta.astype(dtype={"rot1": "str", "rot2": "str", "rot3": "str"})

# Pass ddf_meta to .apply(..., meta=ddf_meta)
ddf.groupby(["bene_id", "hdr_icn"]).apply(agg_func, ["rot1", "rot2", "rot3"], meta=ddf_meta).compute()
```

## Joining on Index + Separate Column

### Setup Data

```python
import pandas as pd
import dask.dataframe as dd

from io import StringIO

ddf1_string = StringIO(
    """hdr_icn_num,ver,col1
1,1,foo
2,1,foo
3,1,foo
4,1,foo
5,1,foo
    """
)
ddf1 = dd.from_pandas(pd.read_csv(ddf1_string, sep=","), 5)
ddf1 = ddf1.set_index("hdr_icn_num")

ddf2_string = StringIO(
    """hdr_icn_num,ver,col2,col3
1,1,bar!,baz
1,2,X,X
2,1,bar!,
2,2,X,X
3,1,bar!,baz
3,2,X,X
4,1,bar!,
4,2,X,X
5,1,bar!,baz
5,2,X,X
    """
)

ddf2 = dd.from_pandas(pd.read_csv(ddf2_string, sep=",", keep_default_na=False), 5)
ddf2 = ddf2.set_index("hdr_icn_num")

ddf1.head(10, ddf1.npartitions)

ddf2.head(10, ddf2.npartitions)
```

### Works

```python
join_df = dd.merge(
    left=ddf1,
    right=ddf2,
    on=["hdr_icn_num"],
    left_on=["hdr_icn_num", "ver"],
    right_on=["hdr_icn_num", "ver"],
    how="left",
)
join_df.head(10, join_df.npartitions)
```

### Works

```python
join_df = dd.merge(
    left=ddf1,
    right=ddf2,
    left_on=["hdr_icn_num", "ver"],
    right_on=["hdr_icn_num", "ver"],
    how="left",
)
join_df.head(10, join_df.npartitions)
```

### Does Not Work

```python
join_df = dd.merge(
    left=ddf1,
    right=ddf2,
    left_index=True,
    right_index=True,
    left_on=["ver"],
    right_on=["ver"],
    how="left",
)
join_df.head(10, join_df.npartitions)
```

## Task / Scheduler Notes

# Run on Scheduler

`client.run_on_scheduler` takes a custom function. The custom function should include an argument `dask_scheduler` if the custom function requires access to the Scheduler object and its [API](https://distributed.dask.org/en/latest/scheduling-state.html#distributed.scheduler.Scheduler).

```python
client = Client("etcetc")

# shows tasks on workers
client.has_what()

def get_task_stream(dask_scheduler):
    # Shows tasks that have been run/submitted in the past?
    return dask_scheduler.get_task_stream() 
    
def kill_task_across_clients(dask_sheduler, task_key):
    # Kill some task that exist w/some client
    # task_key == 'etc_etc-c07efb0ea6dd8c15df9a948ccd19e28c'
    for client in dask_scheduler.clients:
        dask_scheduler.cancel_key(key=task_key, client=client)
    
task_stream = client.run_on_scheduler(get_task_stream)

def user_info() -> dict:
    """
    Returns dict of user information for the current process.

    Returns: Dict
    """
    import os
    import getpass

    return dict(
        uid=os.geteuid(),
        gid=os.getgid(),
        egid=os.getegid(),
        groups=os.getgroups(),
        user=getpass.getuser(),
    )

# Retrieve user info for the scheduler owner
client.run_on_scheduler(user_info)
user_info()
```
