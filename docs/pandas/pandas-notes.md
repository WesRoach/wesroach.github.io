# Pandas Notes

## Data Structures

- Indexes: Sequence of labels
	- Immutable (Like dictionary keys
	- Homogenous in data type (Like NumPy array)
- Series: 1D array with Index
- DataFrames: 2D array with Series as columns

## Index

### Index Examples

```python
import pandas as pd
prices = [10.70, 10.86, 10.74, 10.71, 10.79]
shares = pd.Series(prices) 
days = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri']
pd.Series(prices, index=days)
shares.index.name = 'weekday'
# Indivdual elements in index are immutable
shares.index[2] = 'Wednesday' #error
# entire index can be re-built
shares.index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
```

## Index Multiple Values

Indexes can be built with multiple values using tuples

```python
df = df.set_index(['col1', 'col2'])
print(df.index.name)
=> None
print(df.index.names)
=> ['col1', 'col2']
```

## Index Sorting

```python
df = df.sort_index()
```

## df.loc 

```python
stocks.loc[('CSCO', '2016-10-04')] # returns all columns
stocks.loc[('CSCO', '2016-10-04'), 'col1'] # returns col1
stocks.loc['CSCO'] # returns rows within 'CSCO' index
stocks.loc['CSCO':'MSFT'] # returns rows with index b/t
stocks.loc[(['AAPL', 'MSFT'], '2016-10-05']), :]
stocks.loc[(['AAPL', 'MSFT'], '2016-10-05'), 'Close']
stocks.loc[('CSCO', ['2016-10-05', '2016-10-03']), :]
```

### Slicing (both indexes)

```python
stocks.loc[(slice(None), slice('2016-10-03','2016-10-04')), :]

# Look up data for CA and TX in month 2: CA_TX_month2
CA_TX_month2 = sales.loc[(['CA', 'TX'], 2), :]

# Look up data for all states in month 2: all_month2
all_month2 = sales.loc[(slice(None), 2), :]
```



TODO(Wes) - go back to lecture on this

## df.iloc 

TODO(Wes)

## List Comprehensions

TODO(Wes)





























