import duckdb
class DuckDBExecutor:
    def __init__(self):
        self.connection = duckdb.connect()
    def register_datasets(self, datasets):
        for name, df in datasets.items():
            self.connection.register(name, df)
    def execute(self, sql):
        return self.connection.execute(sql).fetchdf()