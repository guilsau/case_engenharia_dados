from sqlalchemy import create_engine
import pandas as pd

class DatabaseConnector:
    def __init__(self, db_path="sqlite:///marketing.db"):
        self.engine = create_engine(db_path)

    def write_table(self, df, table_name, chunksize=50000):
        df.to_sql(table_name, self.engine, if_exists="replace", index=False, chunksize=chunksize)

    def read_table(self, table_name):
        """Lê uma tabela do banco e retorna como DataFrame."""
        return pd.read_sql(f"SELECT * FROM {table_name}", self.engine)