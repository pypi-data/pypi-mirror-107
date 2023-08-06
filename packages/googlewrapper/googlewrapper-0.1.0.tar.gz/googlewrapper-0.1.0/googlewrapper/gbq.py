from google.cloud import bigquery
import pandas_gbq

class GoogleBigQuery():
    def __init__(self,auth):
        self._client = bigquery.Client(credentials = auth)
        self._project = auth.project_id
    
    def set_dataset(self,ds):
        self._dataset = ds
    
    def set_table(self,t):
        self._table = t

    def full_table_name(self):
        return f"{self._dataset}.{self._table}"
    
    def send(self,df,chunk_size = 10000,behavior = 'append',pb = False):
        try:
            df.to_gbq(destination_table = f"{self._dataset}.{self._table}", 
                                project_id = self._project,
                                chunksize = chunk_size,
                                if_exists = behavior,
                                progress_bar = pb)
        except AttributeError as e:
            issue = e.args[0].split("'")[-2].replace('_','')
            raise AttributeError(f"Please run self.set_{issue}('your_{issue}_name_here') before running self.send()")
        
    def read(self):
        pass

    def delete_day(self,d):
        q = f"""
        DELETE  
        FROM `{self._project}.{self._dataset}.{self._table}` 
        
        WHERE 
        EXTRACT(Year FROM `Date`) = {d.year}
        AND
        EXTRACT(Month FROM `Date`) = {d.month}
        AND
        EXTRACT(Day FROM `Date`) = {d.day}
        """
        self._client.query(q)
        return q
