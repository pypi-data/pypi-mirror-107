import pandas as pd

from urllib.parse import quote
from sqlalchemy import create_engine


class MySQL(object):
    """Class to query MySQL database"""

    def __init__(self, username: str, password: str, host: str):
        self.host = host
        self.username = quote(username, safe="!~*'();/?:&=+$,#^_.&<>")
        self.password = quote(password, safe="!~*'();/?:&=+$,#^_.&<>")

    def __engine_mysql(self, schema: str):
        """Private function to create the connection engine"""
        engine = create_engine(
            f'mysql+pymysql://{self.username}:{self.password}@{self.host}/{schema}')

        return engine

    def select_query(self, query: str, schema: str):
        """Queries the database and returns a Dataframe

        Parameters
        ----------
        query : str
            query to be passed on to the database

        schema : str
            Schema in which the tables are located

        Returns
        -------
        pandas DataFrame
        """
        # connection engine
        engine = MySQL.__engine_mysql(self, schema)

        with engine.connect() as conn:
            df = pd.read_sql(query, conn)

        return df
