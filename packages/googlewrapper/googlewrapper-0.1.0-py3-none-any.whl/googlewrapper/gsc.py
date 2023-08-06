import datetime as dt
import pandas as pd

class GoogleSearchConsole():
    def __init__(self,auth):
        self.auth = auth
        self._filter = None
        self._dims = ['page','date']
        self.set_sites()
        self._branded_dict = None

    def set_sites(self,s = None):
        if s == None:
            self._site_list = self.all_sites()
        else:
            self._site_list = s

    def set_dimensions(self,d):
        '''
        d: what we want to break it down by
            type: list
            options: ['page','date','query', 'device','country']
        '''
        self._dims = d

    def set_filters(self,f = None):
        '''
        filters_list: list of filters formated as GSC requires
        example_filter = {
                        "dimension": string,
                        "operator": string,
                        "expression": string
                        }
        '''
        self._filter = f

    def set_start_date(self,d):
        self._s_date = d
    
    def set_end_date(self,d):
        self._e_date = d
        
    def set_branded(self,bd):
        '''
        pass in a dictionary object
        
        keys are GSC url properties
        values are a list of branded strings
        '''
        self._branded_dict = bd

    def all_sites(self,site_filters=None):

        '''
        takes in a gsc_authentication object and will return a list of sites
        that you have in GSC. IT will give you all by default, but if you pass in
        a list of words it will only return those properties that contain your set 
        of words
        '''
        site_list = self.auth.sites().list().execute()
        clean_list = [s["siteUrl"] for s in site_list["siteEntry"]
                        if s["permissionLevel"] != "siteUnverifiedUser"
                            and s["siteUrl"][:4] == "http"]
        if site_filters == None:
            return clean_list
        elif isinstance(site_filters,list):
            return [s for s in clean_list if any(xs in s for xs in site_filters)]

    def build_request(self,
                        agg_type = "auto",
                        limit = 25000,
                        start_row = 0,
                        pull = True
                        ):
        """
        https://developers.google.com/webmaster-tools/
        search-console-api-original/v3/searchanalytics/query

        agg_type: auto is fine can be byPage or byProperty
        limit: number of rows to return
        start_row: where to start, if need more than 25,000
        """
        
        request_data = {
            "startDate": self._s_date.strftime("%Y-%m-%d"),
            "endDate": self._e_date.strftime("%Y-%m-%d"),
            "dimensions": self._dims,
            "aggregationType" : agg_type,
            "rowLimit": limit,
            "startRow": start_row,
            "dimensionFilterGroups": [
            {
            "filters": self._filter
            }
            ]
            
            }
        if pull:
            return self.execute_request(request_data)
        else:
            return request_data

    def execute_request(self, request):
        """Executes a searchAnalytics.query request.
        Args:
            property_uri: The site or app URI to request data for.
            request: The request to be executed.
        Returns:
            An array of response rows.
        """
        return self.auth.searchanalytics().query(
                        siteUrl=self._current_site, body=request).execute()
        
    def clean_resp(self,data):
        '''
        Takes raw response, and cleans the data into a pd.Dataframe
        '''
        df = pd.DataFrame(data["rows"])
        df.index.name = "idx"
        keys = df["keys"].apply(pd.Series)
        keys.columns = self._dims
        df = df.merge(keys,how="left",on="idx")
        df.drop(columns="keys",inplace = True)
        df.columns = df.columns.str.capitalize()
        
        #branded check
        if isinstance(self._branded_dict,dict) and 'Query' in df.columns:
            df['Branded'] = self.check_branded(df['Query'])

        #convert to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        df[['Clicks','Impressions']] = df[['Clicks','Impressions']].astype(int)
            
        return df

    
        return data

    def check_branded(self,query_list):
        return pd.Series(query_list).str.contains('|'.join(self._branded_dict[self._current_site]),na=False)
    
    def get_data(self):
        '''
        will give you all information
        '''
        data ={}
        for x in self._site_list:
            self._current_site = x
            start = 0
            row_limit = 25000
            temp_df = pd.DataFrame()
            while True:
                try:
                    temp_df = temp_df.append(
                                        self.clean_resp(self.build_request(limit = row_limit,start_row = start))
                                        )
                except:
                    break
                start+=row_limit
                
            data[x] = temp_df 
        
        return data
