import pandas as pd
import os
import sys

def extract(filepath: str) -> pd.DataFrame:
    """
    Lit un fichier CSV et retourne un DataFrame.
    Vérifie l'existence du fichier avant lecture.
    """
    if not os.path.exists(filepath):
        print(f"[ERREUR] Le fichier {filepath} est introuvable.")
        sys.exit(1) # Arrêt propre du programme si fichier absent

    try:
        df = pd.read_csv(filepath)
        print(f"[EXTRACT] Chargement de {filepath} : {len(df)} lignes trouvées.")
        return df
    except Exception as e:
        print(f"[ERREUR] Impossible de lire le CSV {filepath} : {e}")
        sys.exit(1)