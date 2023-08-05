import requests
import pandas as pd
import numpy as np

class Fred():
    def __init__(self, api_key):
        self.fred_api_key = api_key
        self.url_ending = f"?&api_key={self.fred_api_key }&file_type=json"
        self.root_url = "https://api.stlouisfed.org/fred/"
        
    def _series_description(self, series):
            desc = self.get_series_info(series)
            print("#" * 6, " Description ","#" * 6, "\n")
            print(f"Title: {desc['title'].values[0]}")
            print(f"Description:\n {desc['notes'].values[0]} \n")
            print(f"Report Frequency: {desc['frequency'].values[0]}" )
            print(f"Units: {desc['units'].values[0]}" )
            print(f"Starting Date: {desc['observation_start'].values[0]}" )
            print(f"Ending Date: {desc['last_updated'].values[0]}" )
            if "seasonal_adjustment" in desc.columns:
                print(f"Seasonal Adjustment: {desc['seasonal_adjustment'].values[0]}" )
            print("\n", "#" * 21, "\n")
        
    ###### Releases #####
    def get_all_releases_dates(self):
        url = f"{self.root_url}/releases/dates{self.url_ending}"
        content = requests.get(url).json()
        return pd.DataFrame(content["release_dates"])
    def get_release_info(self, release_id):
        url = f"{self.root_url}/release{self.url_ending}&release_id={release_id}"
        content = requests.get(url).json()
        return pd.DataFrame(content["releases"])
    def get_release_series(self, release_id):
        url = f"{self.root_url}/release/series{self.url_ending}&release_id={release_id}"
        content = requests.get(url).json()
        return pd.DataFrame(content["seriess"])
    def get_release_tag_name(self, release_id):
        url = f"{self.root_url}/release/tags{self.url_ending}&release_id={release_id}"
        content = requests.get(url).json()
        return pd.DataFrame(content["tags"])
    def get_related_releases(self, release_id, tag_name):
        url = f"{self.root_url}/release/related_tags{self.url_ending}&release_id={release_id}&tag_names={tag_name}"
        content = requests.get(url).json()
        return pd.DataFrame(content["tags"])
    def get_release_source(self, release_id):
        url = f"{self.root_url}/release/sources{self.url_ending}&release_id={release_id}"
        content = requests.get(url).json()
        return pd.DataFrame(content["sources"])
    
    def get_release_table(self, release_id, element_id=None):
        #NSA Annual Table releaseid:53 elementid:41047
        #Quarterly realease:53 element:12998
        url = f"{self.root_url}/release/tables{self.url_ending}&release_id={release_id}"
        if element_id:
            url += f"&element_id={element_id}"
        content = requests.get(url).json()
        return pd.DataFrame(content["elements"]).T
    
    ###### Series #######
    
    def get_series_info(self, series_id, description=False):
        url = f"{self.root_url}/series{self.url_ending}&series_id={series_id}"
        content = requests.get(url).json()
        if description:
            self._series_description(series_id)
    
        return pd.DataFrame(content["seriess"])
    
    def get_series_value(self, series_id):
        url = f"{self.root_url}/series/observations{self.url_ending}&series_id={series_id}"
        content = requests.get(url).json()
        
        if "observations" not in content.keys(): return pd.DataFrame()
        df = pd.DataFrame(content["observations"])
        
        if "realtime_start" in df.columns:
            df.drop("realtime_start", axis=1, inplace=True)
        if "realtime_end" in df.columns:
            df.drop("realtime_end", axis=1, inplace=True)

        if len(df) > 0:
            df["date"] = pd.to_datetime(df["date"]) 
        
        return df
    
    
    ### Custom series
    def get_custom_series(self, series, description=False):
        series = series.upper()
        
        series_translation = "GDP"
        
        if series == "GDP":
            series_translation = "GDPA"
        elif series == "GDP-Q":
            series_translation = "GDP"
        
        df = self.get_series_value(series_translation)
        
        if description:
            self._series_description(series_translation)
            
        return df
    
    def search_for_series(self, keywords):
        keywords = keywords.replace(" ", "+")
        url = f"{self.root_url}/series/search{self.url_ending}&search_text={keywords}"
        content = requests.get(url).json()
        if "seriess" not in content.keys():
            return pd.DataFrame()
        return pd.DataFrame(content["seriess"])
    
    def get_series_updates(self):
        url = f"{self.root_url}/series/updates{self.url_ending}"
        content = requests.get(url).json()
        return pd.DataFrame(content["seriess"])
