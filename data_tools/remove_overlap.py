import os
import argparse
from obspy import read

def test_overlap(st):
    result = st.get_gaps() 
    for r in result:
        if r[6] < 0:
            return True
    return False

def merge_sds_files(sds_directory, station_filters, year_filters, verbose=False):
    for root, dirs, files in os.walk(sds_directory):
        for file in files:
            parts = file.split('.')
            if len(parts) != 7:
                continue

            _, sta, _, _, _, year, _ = parts
            
            if sta in station_filters or station_filters == []:
                if year in year_filters or year_filters == []:
                    file_path = os.path.join(root, file)
                    
                    try:
                        st = read(file_path)
                    except Exception as e:
                        if verbose:
                            print(f"Erreur lors de la lecture du fichier {file_path}: {e}")
                        continue
                    
                    if test_overlap(st):
                        if verbose:
                            print(f"Overlaps trouvés dans le fichier {file_path}")
                        st.merge(method=-1)
                        
                        # Réécrire le fichier s'il y a eu des modifications
                        try:
                            st.write(file_path, format='MSEED')
                            if verbose:
                                print(f"Fichier fusionné réécrit: {file_path}")
                        except Exception as e:
                            print(f"Erreur lors de l'écriture du fichier {file_path}: {e}")
                    else:
                        if verbose:
                            print(f"Aucun overlap trouvé dans le fichier: {file_path}")

def main():
    parser = argparse.ArgumentParser(description="Merge des fichiers SDS avec obspy. Exemple: python script.py /chemin/vers/votre/SDS --stations STA1 STA2 --years 2021 2022")
    parser.add_argument("--sds", type=str, help="Chemin vers le répertoire SDS.")
    parser.add_argument("--station", nargs="+", default=[], help="Liste des stations à filtrer.")
    parser.add_argument("--year", nargs="+", default=[], help="Liste des années à filtrer.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Afficher les messages détaillés.")

    args = parser.parse_args()

    merge_sds_files(args.sds, args.station, args.year, verbose=args.verbose)
    
if __name__ == "__main__":
    main()
