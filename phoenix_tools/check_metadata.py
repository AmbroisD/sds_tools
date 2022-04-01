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
        #self._get_channels()


    def _get_channels(self):
        """
        """
        self.channels = self.PHOENIX_DB.get_table_objects("channel", filter_select = ("station_fk", self.station.object_id()))

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

    def _check_seed_norme(self) -> None:
        """[summary]
           network: 2
           station: 5
           location: 2

        Channel:
           BAND_SOURCE_POSITION”, where
           BAND indicates the general sampling rate and response band of the data source
           SOURCE is a code identifying an instrument or other data producer and
           POSITION is a code identifying orientation or otherwise relative position
           Uppercase [A-Z]
           Numeric [0-9]

           1 letter
           F ... ≥ 1000 to < 5000 ≥ 10 sec
           G ... ≥ 1000 to < 5000 < 10 sec
           D ... ≥ 250 to < 1000 < 10 sec
           C ... ≥ 250 to < 1000 ≥ 10 sec
           E Extremely Short Period ≥ 80 to < 250 < 10 sec
           S Short Period ≥ 10 to < 80 < 10 sec
           H High Broadband ≥ 80 to < 250 ≥ 10 sec
           B Broadband ≥ 10 to < 80 ≥ 10 sec
           M Mid Period > 1 to < 10
           L Long Period ≈ 1
           V Very Long Period ≈ 0.1
           U Ultra Long Period ≈ 0.01
           R Extremely Long Period ≥ 0.0001 to < 0.001
           P On the order of 0.1 to 1 day[1] ≥ 0.00001 to < 0.0001
           T On the order of 1 to 10 days[1] ≥ 0.000001 to < 0.00001
           Q Greater than 10 days[1] < 0.000001

           2 letters pour Seismometer
           H High Gain Seismometer
           L Low Gain Seismometer
           G Gravimeter
           M Mass Position Seismometer
           N Accelerometer

           3 letter
           Z N E Traditional (Vertical, North-South, East-West), when with 5 degrees of true directions
           A B C Triaxial (Along the edges of a cube turned up on a corner)
           T R For formed beams or rotated components (Transverse, Radial)
           1 2 3 Orthogonal components but non traditional orientations
           U V W Optional components

        """
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
        return self.report
        
        #self.report["station_exist"] = station_exist
            







