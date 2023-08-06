import inflection
import pandas as pd


class DataCleaning():
    """Class to perform transformations in dataframes"""

    def __init__(self):
        pass

    def rename_dataframe_snakecase(self, df):
        """Rename a dataframe with a snake case pattern and returns a Dataframe

        Parameters
        ----------
        df : pandas DataFrame
            DataFrame to be renamed

        Returns
        -------
        pandas DataFrame
        """
        def snakecase(col): return inflection.underscore(col)
        new_columns = list(map(snakecase, df.columns))

        df.columns = new_columns
        return df

    def rename_dataframe_camelcase(self, df):
        """Rename a dataframe with a camel case pattern and returns a Dataframe

        Parameters
        ----------
        df : pandas DataFrame
             DataFrame to be renamed

        Returns
        -------
        pandas DataFrame
        """
        def camelcase(col): return inflection.camelize(col)
        new_columns = list(map(camelcase, df.columns))

        df.columns = new_columns
        return df