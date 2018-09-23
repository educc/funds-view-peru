import pandas
import json
from datetime import datetime

class AlgoTransform:
    COL_DATE = "date"
    COL_VALUE = "value"

    def create(self, raw_data: str):
        jsondata = json.loads(raw_data)
        
        for item in jsondata["quotes"]:
            item[self.COL_DATE] = datetime.strptime(item[self.COL_DATE], "%d/%m/%Y")
        
        df = pandas.DataFrame.from_dict(jsondata["quotes"])
        #df = df.set_index([self.COL_DATE])
        return df

    def process(self, data_frame: pandas.DataFrame):
        """
            this returns a revenue = pandas Number
        """
        return None
#end-class