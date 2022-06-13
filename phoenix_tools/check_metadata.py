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
        self.channel_exist = True
        self.report = {"name" : self.name}
        
        self._get_station()
        self._get_channels()


    def _get_channels(self):
        """
        """
        self.channels = self.PHOENIX_DB.get_table_objects("channel", filter_select = ("station_fk", self.station.object_id()))
        print(len(self.channels))        

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
             

    def _channel_exist(self) -> None:
        pass

    def _channel_open(self, date: list) -> None:
        pass

    def _check_period(self) -> None:
        pass

    def _check_sampling_rate(self) -> None:
        pass

    def get_report(self, level="ERROR") -> dict:
        """
        3 levels : INFO, WARNING, ERROR
        """
        pass
    
    def check_metadata(self):
        """
        """
        self.report["station_exist"] = self.station_exist
        self.report["list_channel"] = self.channels
        return self.report
        
        #self.report["station_exist"] = station_exist
            







