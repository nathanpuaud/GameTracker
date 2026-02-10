import os
from datetime import datetime
from decimal import Decimal
from src.database import database_connection
from src.config import Config  # <-- pour récupérer le nom exact de la BDD (etl_db)

OUTPUT_PATH = "output/rapport.txt"

def _fmt_avg(value):
    if value is None:
        return "N/A"
    if isinstance(value, Decimal):
        value = float(value)
    return f"{round(value, 2)}"

def generate_report():
    # Dossier output/
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    dbname = getattr(Config, "MYSQL_DATABASE", None) or getattr(Config, "DB_NAME", None) or "etl_db"
    # On qualifie systématiquement les tables avec le schéma (dbname.table)
    tbl_players = f"{dbname}.players"
    tbl_scores  = f"{dbname}.scores"

    with database_connection() as conn:
        # buffered=True pour éviter des "Unread result" si on enchaîne
        cur = conn.cursor(buffered=True)

        # Sanity check : quelle base est sélectionnée par défaut ?
        cur.execute("SELECT DATABASE();")
        current_db = cur.fetchone()[0]
        print(f"[REPORT] Base courante: {current_db} | Schéma utilisé: {dbname}")

        # 1) Statistiques générales
        cur.execute(f"SELECT COUNT(*) FROM {tbl_players};")
        nb_players = cur.fetchone()[0] or 0

        cur.execute(f"SELECT COUNT(*) FROM {tbl_scores};")
        nb_scores = cur.fetchone()[0] or 0

        cur.execute(f"SELECT COUNT(DISTINCT game) FROM {tbl_scores};")
        nb_games = cur.fetchone()[0] or 0

        # 2) Top 5 des meilleurs scores (score, game, username)
        cur.execute(
            f"""
            SELECT s.score, s.game, p.username
            FROM {tbl_scores} AS s
            INNER JOIN {tbl_players} AS p ON p.player_id = s.player_id
            ORDER BY s.score DESC
            LIMIT 5;
            """
        )
        top5 = cur.fetchall()

        # 3) Score moyen par jeu
        cur.execute(
            f"""
            SELECT game, AVG(score) AS avg_score
            FROM {tbl_scores}
            GROUP BY game
            ORDER BY avg_score DESC;
            """
        )
        avg_scores = cur.fetchall()

        # 4) Répartition des joueurs par pays
        cur.execute(
            f"""
            SELECT
                COALESCE(NULLIF(TRIM(country), ''), 'Inconnu') AS country,
                COUNT(*) AS cnt
            FROM {tbl_players}
            GROUP BY country
            ORDER BY cnt DESC, country ASC;
            """
        )
        players_per_country = cur.fetchall()

        # 5) Répartition des sessions par plateforme
        cur.execute(
            f"""
            SELECT
                COALESCE(NULLIF(TRIM(platform), ''), 'Inconnu') AS platform,
                COUNT(*) AS cnt
            FROM {tbl_scores}
            GROUP BY platform
            ORDER BY cnt DESC, platform ASC;
            """
        )
        sessions_per_platform = cur.fetchall()

    # Écriture du rapport
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append("====================================================")
    lines.append("GAMETRACKER - Rapport de synthese")
    lines.append(f"Genere le : {now_str}")
    lines.append("====================================================")
    lines.append("")   # saut de ligne

    lines.append("--- Statistiques generales ---")
    lines.append(f"Nombre de joueurs : {nb_players}")
    lines.append(f"Nombre de scores : {nb_scores}")
    lines.append(f"Nombre de jeux : {nb_games}")
    lines.append("")   # saut de ligne

    lines.append("--- Top 5 des meilleurs scores ---")
    if top5:
        for i, (score, game, username) in enumerate(top5, start=1):
            lines.append(f"{i}. {username} | {game} | {score}")
    else:
        lines.append("Aucun score disponible")

    lines.append("")   # saut de ligne
    lines.append("--- Score moyen par jeu ---")
    if avg_scores:
        for game, avg in avg_scores:
            lines.append(f"{game} : {_fmt_avg(avg)}")
    else:
        lines.append("Aucun jeu disponible")

    lines.append("")   # saut de ligne
    lines.append("--- Joueurs par pays ---")
    if players_per_country:
        for country, cnt in players_per_country:
            lines.append(f"{country} : {cnt}")
    else:
        lines.append("Aucun joueur enregistre")
        
    lines.append("")   # saut de ligne
    lines.append("--- Sessions par plateforme ---")
    if sessions_per_platform:
        for platform, cnt in sessions_per_platform:
            lines.append(f"{platform} : {cnt}")
    else:
        lines.append("Aucune session enregistree")

    lines.append("====================================================")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"[REPORT] Rapport genere dans {OUTPUT_PATH}")