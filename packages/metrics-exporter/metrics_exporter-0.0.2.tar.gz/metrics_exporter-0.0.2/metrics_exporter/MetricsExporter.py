from typing import Dict, List, cast
import psycopg2
import psycopg2.extras

class MetricsExporter:
    __connection = None
    __bufferSize = 10000
    __bufferMetrics: List[List[float]] = []
    __metricsAcc: List[Dict[str, float]] = []
    __metricsNames: List[str] = []
    __insertSqlNames: str
    __bufferLen = 0
    __bufferSize = 10000
    __tableName: str

    def __init__(self,
            metricsGroups: List[List[str]],
            tableName: str,
            user: str,
            password: str,
            dbname: str = 'postgres',
            host: str = 'localhost',
            port: int = 5432,
            bufferSize: int = 10000
        ):
        self.__connection = psycopg2.connect(f"dbname='{dbname}' user='{user}' host='{host}' password='{password}' port={port}")
        self.__bufferSize = bufferSize
        self.__tableName = tableName

        self.__metricsAcc = []
        self.__metricsNames = []
        for metricGroup in metricsGroups:
            d: Dict[str, float] = {}
            for m in metricGroup:
                d[m] = 0
            self.__metricsAcc.append(d)
            self.__metricsNames += metricGroup

        allMetrics = self.__getAllMetrics(self.__metricsNames)
        self.__insertSqlNames = f"(id, name, yearmonth, {', '.join(allMetrics)}) VALUES (%s, %s, %s, {', '.join(map(lambda _: '%s', allMetrics))})"

    def __getAllMetrics(self, metrics: List[str]) -> List[str]:
        m = map(lambda x: [f"{x}_ASS", f"{x}_NORM", f"{x}_ASS_ACC", f"{x}_NORM_ACC"], metrics)
        return [item for sublist in m for item in sublist]

    def insertMetric(self, id: int, name: str, month: str, values: List[Dict[str, float]]):

        newMetric: List = []

        x = zip(values, self.__metricsAcc)
        for x in zip(values, self.__metricsAcc):
            currMetrics = x[0]
            currAcc = x[1]
            for m in currMetrics:
                currAcc[m] += currMetrics[m]

            curTot = sum(currMetrics.values())
            accTot = sum(currAcc.values())

            for m in currMetrics:
                newMetric += [currMetrics[m], currAcc[m], currMetrics[m] / curTot, currAcc[m] / accTot]

        self.__bufferMetrics.append(cast(List, [id, name, month]) + newMetric)
        self.__bufferLen += 1

        if (self.__bufferLen > self.__bufferSize):
            self.__insertBuffer()

    def finalize(self):
        self.__insertBuffer()

    def __insertBuffer(self):
        cur = self.__connection.cursor()
        if (len(self.__bufferMetrics) > 0):
            psycopg2.extras.execute_batch(cur, f"INSERT INTO {self.__tableName} {self.__insertSqlNames}", self.__bufferMetrics)
            self.__connection.commit()
        cur.close()
        self.__bufferMetrics = []
        self.__bufferLen = 0

    def createTable(self):
        cur = self.__connection.cursor()
        metricSql = ", ".join(map(lambda x: f"{x} double precision", self.__getAllMetrics(self.__metricsNames)))
        sql = f"CREATE TABLE {self.__tableName} (id integer NOT NULL, name character varying NOT NULL, yearmonth character(7) NOT NULL, {metricSql}, PRIMARY KEY (id, name, yearmonth) );"
        cur.execute(sql)
        self.__connection.commit()
        self.__bufferMetrics = []
        self.__bufferLen = 0
        cur.close()

    def dropTables(self):
        cur = self.__connection.cursor()
        cur.execute(f"DROP TABLE IF EXISTS {self.__tableName}")
        self.__bufferMetrics = []
        self.__bufferLen = 0
        self.__connection.commit()
        cur.close()

    def getMetrics(self):
        return self.__bufferMetrics
