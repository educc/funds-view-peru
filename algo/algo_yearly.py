import pandas
import numpy as np
from algo.algo_transform import AlgoTransform


def calculate_revenue(row):
    first = row[AlgoYearly.COL_FIRST]
    last = row[AlgoYearly.COL_LAST]
    return (last-first)*100/first

class AlgoYearly(AlgoTransform):
    COL_YEAR = "date_year"
    COL_YEAR_MONTH = "date_year_month"
    COL_REVENUE = "revenue"
    COL_FIRST = "first"
    COL_LAST = "last"
    
    def process(self, df:pandas.DataFrame):
        df = df[df.value != 0] #remove zero values

        if df.empty:
            return 0
        
        df = self.add_columns(df)

        df = df[self.COL_VALUE].groupby(df[self.COL_YEAR]).agg({
            self.COL_FIRST: lambda x: x.iloc[0],
            self.COL_LAST:  lambda x: x.iloc[-1],
        })

        df[self.COL_REVENUE] = df.apply(calculate_revenue, axis=1)
        average = df[self.COL_REVENUE].mean()
        return np.round(average, decimals=2)

    def add_columns(self, df:pandas.DataFrame):
        df[self.COL_YEAR] = df.apply(lambda x: x[self.COL_DATE].strftime("%Y") , axis=1)
        df[self.COL_YEAR_MONTH] = df.apply(lambda x: x[self.COL_DATE].strftime("%Y%m") , axis=1)
        df = df.set_index([self.COL_DATE])
        return df

