import os
import time
import json
import pandas
from algo import AlgoTransform
from algo import AlgoAllTime
from algo import AlgoYearly

_DATA_PATH = "./data"
_FILENAME_FUNDS = "manager_funds.json"

class ManagerProcessData:

    COLUMN_ID = "value"
    COLUMN_NAME = "label"
    COLUMN_REVENUE = "revenue"

    def __init__(self, filename_headers: str):
        self.headers = self._create_headers_dict(filename_headers)
        self.data_processed = None

    #public
    #----------------------------------------------

    def process_all(self, base_path:str , algo: AlgoTransform):
        result = []
        for item in self.headers:
            filename = os.path.join(base_path, item[self.COLUMN_ID])
            filename += ".json"

            p = ProcessData(algo)
            p.create(filename)
            revenue = p.process()

            result.append({
                self.COLUMN_ID: item[self.COLUMN_ID],
                self.COLUMN_NAME: item[self.COLUMN_NAME] + " " + str(revenue),
                self.COLUMN_REVENUE: revenue
            })
        self.data_processed = pandas.DataFrame.from_dict(result) \
                .sort_values([self.COLUMN_REVENUE], ascending=[False])
        return self.data_processed
    
    def save(self):
        self.data_processed.to_csv(ProcessData.OUT_SAVE_FILE, \
            columns=[self.COLUMN_ID, self.COLUMN_NAME, self.COLUMN_REVENUE], \
            index=False, \
            sep=";")

    #private
    #----------------------------------------------
    def _create_headers_dict(self, filename: str):
        result = []
        with open(filename, "r", encoding="utf-8") as myfile:
            jsondata = json.loads(myfile.read())

            for item in jsondata["funds"]:
                custom_value = "%s-%s" % (item["id"], item["manager_code"])
                result.append({
                    self.COLUMN_ID: custom_value,
                    self.COLUMN_NAME:  item["name"]
                })
        #end-with
        return result
#end-class

class ProcessData:

    OUT_SAVE_FILE = "funds_list_ordered.csv"

    def __init__(self, algorith_transform: AlgoTransform):
        self.algo = algorith_transform
        self.dataframe_raw = None
    
    #public
    #----------------------------------------------
    def create(self, filenamedata: str):
        """
            create a dataframe base on AlgoTransform object
        """
        try:
            with open(filenamedata, "r", encoding="utf-8") as myfile:
                self.dataframe_raw = self.algo.create(myfile.read())
            return self.dataframe_raw
        except Exception as ex:
            print(ex)
        return None

    def process(self):
        if self.dataframe_raw is None:
            return None
        return self.algo.process(self.dataframe_raw)

#end-class

def main():
    start = time.time()
    
    algo = AlgoYearly()

    manager = ManagerProcessData(_FILENAME_FUNDS)
    result = manager.process_all(_DATA_PATH, algo)
    print(result)
    manager.save()
  
    end_time = time.time()  
    print("Total time: {}".format(end_time - start))


if __name__ == "__main__":
    main()