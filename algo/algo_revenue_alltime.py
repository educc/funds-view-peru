import pandas
import numpy as np
from algo.algo_transform import AlgoTransform

class AlgoAllTime(AlgoTransform):
    
    def process(self, df:pandas.DataFrame):

        df = df[df.value != 0] #remove zero values

        if df.empty:
            return 0
        
        df = df.iloc[[0, -1]]
        first = df["value"][0]
        last = df["value"][1]
        return np.round(last/first*100)