# -*- coding: utf-8 -*-
"""
Le programme utisera lesrésultats du scan de gaps et de la base pheonix pour comparer données et metadonnée

##TODO feature : pouvoir utiliser un station xml
##FIXME
##BUG
"""
class MetaData(object):
    """
    Class used to compare data and metadata.
    """
    def __init__(self, station: str, network: str, location: str, channel: str) -> None:
        """
        Initialize the class

        network             -- Set
        station             -- Set
        location            -- Set
        channel             -- Set

        """
        self.name = station
        self.network = network
        self.location = location
        self.channel = channel
        self.info = dict()
        self.warning = dict()
        self.error = dict()
        pass

    def retrive_station_info(self) -> None:
        pass

    def _test_net(self) -> None:
        pass

    def _station_exist(self) -> None:
        pass

    def _channel_exist(self) -> None:
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
