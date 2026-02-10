import mysql.connector

def load_players(df, conn):
    """Charge les joueurs en base (Upsert)."""
    cursor = conn.cursor()
    # Requête SQL qui gère les conflits
    query = """
    INSERT INTO players (player_id, username, email, registration_date, country, level)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        username = VALUES(username),
        email = VALUES(email),
        country = VALUES(country),
        level = VALUES(level);
    """
    # Préparation des données sous forme de liste de tuples
    data = []
    for _, row in df.iterrows():
        data.append((
            row['player_id'], 
            row['username'], 
            row['email'], 
            row['registration_date'], 
            row['country'], 
            row['level']
        ))
    
    cursor.executemany(query, data)
    print(f"[LOAD] {cursor.rowcount} joueurs traités.")

def load_scores(df, conn):
    """Charge les scores en base (Upsert)."""
    cursor = conn.cursor()
    query = """
    INSERT INTO scores (score_id, player_id, game, score, duration_minutes, played_at, platform)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        score = VALUES(score),
        duration_minutes = VALUES(duration_minutes),
        platform = VALUES(platform);
    """
    
    data = []
    for _, row in df.iterrows():
        data.append((
            row['score_id'], 
            row['player_id'], 
            row['game'], 
            row['score'], 
            row['duration_minutes'], 
            row['played_at'], 
            row['platform']
        ))
    
    cursor.executemany(query, data)
    print(f"[LOAD] {cursor.rowcount} scores traités.")