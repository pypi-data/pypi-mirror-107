import inflection
import pandas as pd


class DataCleaning():
    def __init__(self):
        pass

    def rename_dataframe_snakecase(self, df):
        def snakecase(col): return inflection.underscore(col)
        new_columns = list(map(snakecase, df.columns))

        df.columns = new_columns
        return df

    def rename_dataframe_camelcase(self, df):
        def camelcase(col): return inflection.camelize(col)
        new_columns = list(map(camelcase, df.columns))

        df.columns = new_columns
        return df
