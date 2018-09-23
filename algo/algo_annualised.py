import pandas
import numpy as np
from algo.algo_transform import AlgoTransform


def year_from_date(row):
    value = row[AlgoTransform.COL_DATE].strftime("%Y")
    #print(type(value), value)
    return value

class AlgoAnnualised(AlgoTransform):
    
    def process(self, df:pandas.DataFrame):
        df = df[df.value != 0] #remove zero values

        if df.empty:
            return 0
        
        #df = self.add_columns(df) 

        first = df[self.COL_VALUE].iloc[0]
        last = df[self.COL_VALUE].iloc[-1]

        first_date = df[self.COL_DATE].iloc[0]
        last_date = df[self.COL_DATE].iloc[-1]

        diff = last_date - first_date
        diff = diff.days
        
        result = np.power(last/first,  365.0/diff)-1.0
        return np.round(result*100, decimals=2)

    def add_columns(self, df:pandas.DataFrame):
        return df

