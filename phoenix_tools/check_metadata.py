# -*- coding: utf-8 -*-
"""
Le programme utisera lesrésultats du scan de gaps et de la base pheonix pour comparer données et metadonnée

##TODO feature : pouvoir utiliser un station xml
##FIXME
##BUG
On initialise la class
meta = Metadata(net, sta, loc, channel)
if meta.exist():
else:

1) La station existe dans les metadonnées
2) La station est ouverte
3) Le channel existe
4) Le channel est ouvert
5) 


"""
import pandas as pd
from datetime import datetime
from oca.database.abstractdb import DatabaseObjectFactory


class MetaDataCheck(object):
    """
    Class used to compare data and metadata.
    """
    def __init__(self, station: str) -> None:

        """
        Initialize the class

        station             -- Set station name

        """


        self.HOST = 'babel.unice.fr'
        self.USER = 'sysop'
        self.DB_NAME = 'phoenix'

        self.PHOENIX_DB = DatabaseObjectFactory(self.HOST,
                                                self.USER,
                                                database=self.DB_NAME)

        self.name = station
        self.station = None
        self.station_exist = True
        self.channels = None
        self.df_channels = None
        self.channel_exist = True
        self.report = {"name" : self.name}
        
        self._get_station()
        self._get_channels()


    def _get_channels(self):
        """
        """
        self.channels = self.PHOENIX_DB.get_table_objects("channel", filter_select = ("station_fk", self.station.object_id()))
        
        # Create DataFrame
        df = pd.DataFrame(columns=['station', 'location', 'channel', 'open', 'close', 'comment'])
        
        for channel in self.channels:
            close_date = channel.close_date()
            if close_date is None:
                close_date = datetime.strptime("2999-01-01", "%Y-%m-%d")
            open = datetime(channel.open_date().year, channel.open_date().month, channel.open_date().day, 0, 0, 0) # Set the time at the beginning of the day
            new_channel = {'station' : self.name, 
                          'location': channel.location_code(), 
                          'channel' : channel.iris_code(), 
                          'open': open,
                          'close': close_date, 
                          'comment': channel.comments()}
            df = pd.concat([df, pd.DataFrame.from_records([new_channel])], ignore_index=True)
        
        self.df_channels = df.sort_values('open')

    def _get_station(self):
        station = self.PHOENIX_DB.get_table_objects("station", filter_select = ("iris_code", self.name))
        
        if len(station) == 0:
            self.station_exist = False
        else:
            self.station = station[0]

    def _station_open(self, date: list) -> None:
        """
        plusieur cas 
        1) period ok
        2) la period n'est pas bonne
        3) le debut ou la fin ne sont pas exactement les memes(marge d'erreur)
        """
        start_period = date[0]
        end_period = date[1] 
             

    def channel_exist(self) -> None:
        pass

    def channel_open(self, date: list) -> None:
        pass

    def _check_sampling_rate(self) -> None:
        pass

    def get_report(self, level="ERROR") -> dict:
        """
        3 levels : INFO, WARNING, ERROR
        """
        pass
    
    def check_channel_period(self, location: str, channel: str, date: str) -> None:
        """Verify if channel period exist in database

        :param location: set location code
        :type location: str
        :param channel: set channel code
        :type channel: str
        :param date: set date (format :  "%Y.%j")
        :type date: str
        """
        date = datetime.strptime(date, "%Y.%j")
        
        period = self.df_channels.loc[(self.df_channels["location"] == location) &
                                      (self.df_channels['channel'] == channel) &
                                      (self.df_channels['open'] <= date) &
                                      (self.df_channels['close'] >= date)]
  
        #print(period['close'])
        #period = period.loc[(period['close'] == None)]
        
        if len(period) == 0:
            return False
        else:
            return True
        
    
    def check_metadata(self):
        """
        """
        self.report["station_exist"] = self.station_exist
        #self.report["list_channel"] = self.channels
        self.check_channel_period("00", "ENZ", "2006-05-08")
        return self.report
        
        #self.report["station_exist"] = station_exist
            







