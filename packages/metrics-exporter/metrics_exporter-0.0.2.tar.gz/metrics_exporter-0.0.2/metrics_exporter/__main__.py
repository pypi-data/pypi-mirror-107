from .MetricsExporter import MetricsExporter

if __name__ == "__main__":
    me = MetricsExporter(
            metricsGroups=[['felicità', 'gioia'], ['revertAdmin', 'reverMerde']],
            tableName='it',
            user='root',
            password='root',
            dbname='postgres',
            host='localhost',
            port=5432,
            bufferSize=10000
        )

    me.insertMetric(
        1, 'pippo', '201005',
        [{
            'felicità': 2,
            'gioia': 4
        }, {
            'revertAdmin': 2,
            'reverMerde': 4
        }]
    )

    me.insertMetric(
        1, 'pippo', '201006',
        [{
            'felicità': 4,
            'gioia': 4
        }, {
            'revertAdmin': 2,
            'reverMerde': 4
        }]
    )

    me.finalize()