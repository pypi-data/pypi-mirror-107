# metrics_exporter

## How to use
Set the metrics names and the postgres connection:
```python
me = MetricsExporter(
    metricsGroups=[['metric1', 'metric2'], ['metric3']],
    tableName='it',
    user='root',
    password='root',
    dbname='postgres',
    host='localhost',
    port=5432,
    bufferSize=10000
)
```
For each metrics, 3 other metrics will be calculated:
* Nomamlized value over the metric group
* Accumulated value of the metric
* Normalized accumulated value over the metric group

Now you can insert a new metric for a month in a page/user:
```python
me.insertMetric(
    1, 'pippo', '201005',
    [{
        'metric1': 2,
        'metric2': 4
    }, {
        'metric3': 2
    }]
)
```

To be sure that all metrics have been saved to the database in the end run:
```python
me.finalize()
```


## Pip package
To update the pip package
```bash
python setup.py sdist
twine upload dist/*
```