import pandas as pd

from urllib.parse import quote
from pymongo import MongoClient


class MongoDB(object):
    """Class to query the MongoDB database through pipelines"""

    def __init__(self, username: str, password: str, host_string: str):
        self.username = quote(username, safe="!~*'();/?:@&=+$,#^_.&<>")
        self.password = quote(password, safe="!~*'();/?:@&=+$,#^_.&<>")
        self.host_string = quote(host_string, safe="!~*'();/?:@&=+$,#^_.&<>")

    def __client(self):
        """Private function to create the mongodb client"""
        client = MongoClient(
            f'mongodb+srv://{self.username}:{self.password}@{self.host_string}')

        return client

    def select_pipeline(self, database: str, collection: str, pipeline: list):
        """Queries the database and returns a Dataframe

        Parameters
        ----------
        database : str
           Database to be connected

        collection : str
            Collection in which you want to make the query

        pipeline : list
            Agregation pipeline  (Mongo)

        Returns
        -------
        pandas DataFrame
        """
        client = MongoDB.__client(self)

        db = client[database]
        col = db[collection]

        results = col.aggregate(pipeline)
        df = pd.DataFrame(results)

        return df
