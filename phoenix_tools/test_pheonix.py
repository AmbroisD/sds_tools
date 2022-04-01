import sys
sys.path.insert(0, '/u/leros/SISMO/PRETRAITEMENT/David/abstractdb')
sys.path.insert(0, '/u/leros/SISMO/PRETRAITEMENT/David/pygraph')

from oca.database.abstractdb import DatabaseObjectFactory
from phoenix_tools.check_metadata import MetaDataCheck

HOST = 'babel.unice.fr'
USER = 'sysop'
DB_NAME = 'phoenix'

#PHOENIX_DB = DatabaseObjectFactory(HOST, USER, database=DB_NAME)

stations = ['ARNL', 'ISPT', 'ACH2', 'AV21', 'AES1', 'MORR', 'GYE2', 'FER1', 'ALJ1', 'ATON', 'ISPG', 'VCH1', 'ACH1', 'FER2', 'GYE1', 'AES2', 'ALAH', 'ALOR', 'LGCB', 'ACUE', 'APED', 'FLFR', 'ALIB', 'PPLP', 'ACHN', 'AMNT', 'MILO', 'ALIT', 'CEAZ', 'CABP', 'AZOG', 'ABAB', 'SALI', 'SEVS', 'JAMA', 'ADUR', 'PVIL', 'RVRD', 'MAG1', 'PTGL', 'ALBE', 'ASAM', 'GYE3', 'BV15', 'PDNS', 'APO2', 'ASDO', 'PECV', 'AATC', 'ACAL', 'BALZ', 'APLA', 'AMTV', 'AMAC', 'COHC', 'GOLV', 'ALCE', 'AMA1', 'AZAM', 'APO1'] 


all_station = ['ARIO', 'SEVS', 'MCRA', 'BOSC', 'APR2', 'GGPT', 'ALIT', 'ADUR', 'MORR', 'ALAH', 'AMIL', 'CASC', 'ACAL', 'AOTA', 'FER2', 'CAB1', 'POND', 'APS4', 'MARI', 'APS1', 'GONZ', 'CUSW', 'CHMA', 'VCH1', 'BONI', 'AV03', 'GOLV', 'AAM2', 'CABP', 'ISPT', 'TERV', 'APR1', 'AV11', 'SALI', 'AMTV', 'CHL1', 'ALAT', 'AQUE', 'JUA2', 'AAT1', 'APO2', 'COHC', 'ATUL', 'ACHN', 'NAS2', 'AMCR', 'YAHU', 'AMON', 'APLA', 'FER1', 'CAMI', 'AZAM', 'ECEN', 'LGCB', 'PULU', 'GYE2', 'PTVL', 'APSY', 'ARNL', 'AOTA', 'ACOC', 'PECV', 'ZUMB', 'LNGL', 'CHIB', 'ATEN', 'FLFR', 'AMCR', 'SRAM', 'ANTS', 'AV05', 'SADP', 'LOLA', 'GGPC', 'CRPG', 'HSPR', 'ATON', 'JAMA', 'PVIL', 'AIB2', 'YANA', 'ABAB', 'VC1', 'BRRN', 'ALOR', 'FER2', 'TST1', 'QUIN', 'CAYA', 'SLOR', 'LOJ1', 'RETU', 'ACH1', 'LITA', 'ANTM', 'AV21', 'CHSH', 'TULM', 'ACRM', 'CONE', 'APS4', 'HPAL', 'BUCE', 'ASDO', 'QUEV', 'ILLI', 'AZOG', 'PAST', 'SADP', 'AAM1', 'CAYR', 'MILO', 'ALCE', 'BALZ', 'SUCR', 'GONZ', 'SAGA', 'AMOM', 'MAG1', 'ABH2', 'URCU', 'AOLM', 'PILA', 'BV15', 'JUI6', 'AATC', 'PTCY', 'COTA', 'MCRA', 'PPLP', 'PDNS', 'AES2', 'APJN', 'ALAH', 'ARDO', 'TAMB', 'ACAL', 'BOCA', 'ANTI', 'CEAZ', 'AIB1', 'APUY', 'AGYE', 'PORT', 'FLF1', 'AV18', 'PUYO', 'SAGA', 'TAMH', 'ISPG', 'ACHO', 'TOMA', 'ASAM', 'IGUA', 'ACH2', 'GYE1', 'APR1', 'AES1', 'CUIC', 'ANTG', 'AJPJ', 'AROC', 'BIL2', 'APED', 'AMAC', 'AMNT', 'ACNC', 'CHL2', 'PINO', 'PAC1', 'CUSE', 'RVRD', 'POND', 'ALIB', 'ACUE', 'GYE3', 'APLP', 'SNLR', 'AMAC', 'ALCE', 'APO1', 'ALBE', 'AMA1', 'PTGL', 'VCES', 'ALJ1', 'GYEB', 'PITA', 'CHIS']

def main():
    PHOENIX_DB = DatabaseObjectFactory(HOST, USER, database=DB_NAME)
    ispt = PHOENIX_DB.get_table_objects("station", filter_select = ("iris_code", "RRRR"))
    #ispt_c = PHOENIX_DB.get_table_objects("channel", filter_select = ("station_fk", "769"))
    #print(ispt[0].object_id())
    print(len(ispt))


def get_station():
    PHOENIX_DB = DatabaseObjectFactory(HOST, USER, database=DB_NAME)
    ispt = PHOENIX_DB.get_table_objects("station", filter_select = ("iris_code", "ISPT"))
    ispt_c = PHOENIX_DB.get_table_objects("channel", filter_select = ("station_fk", "769"))
    print(ispt[0].object_id())
    print(len(ispt_c))


 
if __name__ == '__main__':
    for sta in all_station:
        meta = MetaDataCheck(station=sta)
        report = meta.check_metadata()
        print(report)
