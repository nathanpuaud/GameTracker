import pandas as pd
import numpy as np

def transform_players(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie les données des joueurs."""
    df = df.copy()
    
    # Problème : Doublons 
    # On garde la première occurrence du player_id
    df.drop_duplicates(subset=['player_id'], keep='first', inplace=True)
    
    # Problème : Espaces parasites 
    # On utilise .str.strip() pour enlever les espaces parasites
    if 'username' in df.columns:
        df['username'] = df['username'].str.strip()

    # Problème : Dates incohérentes 
    # 'coerce' transforme les dates invalides en NaT
    df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')
    
    # Problème : Emails invalides 
    # Si pas de '@' on remplace par NaN
    if 'email' in df.columns:
        mask_valid_email = df['email'].str.contains('@', na=False)
        df.loc[~mask_valid_email, 'email'] = np.nan

    # Problème : Valeurs manquantes
    # MySQL ne comprend pas 'NaN' de Python, il faut 'None'
    # On remplace tous les NaN par None
    df = df.replace({np.nan: None})
    
    print(f"[TRANSFORM] Joueurs nettoyés : {len(df)} restants.")
    return df

def transform_scores(df: pd.DataFrame, valid_player_ids: list) -> pd.DataFrame:
    """
    Nettoie les scores.
    IMPORTANT : Prend 'valid_player_ids' pour filtrer les orphelins[cite: 124].
    """
    df = df.copy()
    
    # Problème : Doublons sur score_id 
    df.drop_duplicates(subset=['score_id'], keep='first', inplace=True)

    # Conversion numérique (erreurs en NaN) 
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    df['duration_minutes'] = pd.to_numeric(df['duration_minutes'], errors='coerce')
    df['played_at'] = pd.to_datetime(df['played_at'], errors='coerce')

    # Problème : Scores négatifs ou nuls 
    # On ne garde que les lignes où score positif
    df = df[df['score'] > 0]

    # Problème : Valeurs manquantes critiques
    # Si le score ou le joueur est vide, la ligne ne vaut rien
    df.dropna(subset=['score', 'player_id'], inplace=True)

    # Problème : Références orphelines
    # On ne garde que les scores dont le player_id existe vraiment dans la table Players
    initial_count = len(df)
    df = df[df['player_id'].isin(valid_player_ids)]
    orphans_removed = initial_count - len(df)
    if orphans_removed > 0:
        print(f"[TRANSFORM] {orphans_removed} scores orphelins supprimés.")

    # Nettoyage final pour MySQL (NaN -> None)
    df = df.replace({np.nan: None})

    print(f"[TRANSFORM] Scores nettoyés : {len(df)} restants.")
    return df