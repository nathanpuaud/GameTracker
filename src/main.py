from src.database import get_connection
from src.extract import extract
from src.transform import transform_players, transform_scores
from src.load import load_players, load_scores


def main():
    print("=== ETAPE 5 : Orchestration du pipeline ETL ===")

    # --- Connexion à MySQL ---
    print("[MAIN] Connexion à la base...")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1;")
    cursor.fetchone()
    print("[MAIN] Connexion OK !")

    # --- EXTRACT ---
    print("[MAIN] Extraction des CSV...")
    df_players_raw = extract("data/Players.csv") if False else extract("data/raw/Players.csv")
    df_scores_raw = extract("data/Scores.csv") if False else extract("data/raw/Scores.csv")

    # --- TRANSFORM ---
    print("[MAIN] Nettoyage des joueurs...")
    df_players_clean = transform_players(df_players_raw)

    print("[MAIN] Nettoyage des scores...")
    valid_ids = df_players_clean["player_id"].tolist()
    df_scores_clean = transform_scores(df_scores_raw, valid_ids)

    # --- LOAD ---
    print("[MAIN] Chargement des joueurs...")
    load_players(df_players_clean, conn)

    print("[MAIN] Chargement des scores...")
    load_scores(df_scores_clean, conn)

    conn.commit()
    conn.close()

    print("=== ETL TERMINE ===")


if __name__ == "__main__":
    main()