"""
Module de gestion de la base de données SQLite
Gère la persistance des données de tournois, équipes, joueurs et matchs
"""

import sqlite3
import uuid
from typing import List, Dict, Optional
import json


class DatabaseManager:
    """Gestionnaire de base de données SQLite pour Pétanque Manager"""

    def __init__(self, db_path: str = "petanque_manager.db"):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        """Retourne une connexion à la base de données"""
        conn = sqlite3.connect(
            self.db_path,
            uri=self.db_path.startswith("file:")
        )
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Initialise la base de données et crée les tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Table des tournois
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tournaments (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    num_courts INTEGER NOT NULL,
                    status TEXT DEFAULT 'created',
                    current_round INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Table des équipes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS teams (
                    id TEXT PRIMARY KEY,
                    tournament_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    players TEXT,
                    wins INTEGER DEFAULT 0,
                    losses INTEGER DEFAULT 0,
                    points_for INTEGER DEFAULT 0,
                    points_against INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (tournament_id) REFERENCES tournaments (id)
                )
            ''')

            # Table des matchs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS matches (
                    id TEXT PRIMARY KEY,
                    tournament_id TEXT NOT NULL,
                    round_number INTEGER NOT NULL,
                    team1_id TEXT NOT NULL,
                    team2_id TEXT NOT NULL,
                    team1_score INTEGER DEFAULT 0,
                    team2_score INTEGER DEFAULT 0,
                    court_number INTEGER,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (tournament_id) REFERENCES tournaments (id),
                    FOREIGN KEY (team1_id) REFERENCES teams (id),
                    FOREIGN KEY (team2_id) REFERENCES teams (id)
                )
            ''')

            conn.commit()

    # CRUD pour Tournois
    def create_tournament(self, name: str, tournament_type: str, num_courts: int) -> str:
        """Crée un nouveau tournoi"""
        tournament_id = str(uuid.uuid4())
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tournaments (id, name, type, num_courts)
                VALUES (?, ?, ?, ?)
            ''', (tournament_id, name, tournament_type, num_courts))
            conn.commit()
        return tournament_id

    def get_tournament(self, tournament_id: str) -> Optional[Dict]:
        """Récupère un tournoi par son ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tournaments WHERE id = ?', (tournament_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all_tournaments(self) -> List[Dict]:
        """Récupère tous les tournois"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tournaments ORDER BY created_at DESC')
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def update_tournament(self, tournament_id: str, **kwargs):
        """Met à jour un tournoi"""
        if not kwargs:
            return

        set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [tournament_id]

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                UPDATE tournaments
                SET {set_clause}, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', values)
            conn.commit()

    def delete_tournament(self, tournament_id: str):
        """Supprime un tournoi et toutes les données associées"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM matches WHERE tournament_id = ?', (tournament_id,))
            cursor.execute('DELETE FROM teams WHERE tournament_id = ?', (tournament_id,))
            cursor.execute('DELETE FROM tournaments WHERE id = ?', (tournament_id,))
            conn.commit()

    # CRUD pour Équipes
    def create_team(self, tournament_id: str, name: str, players: List[str]) -> str:
        """Crée une nouvelle équipe"""
        team_id = str(uuid.uuid4())
        players_json = json.dumps(players)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO teams (id, tournament_id, name, players)
                VALUES (?, ?, ?, ?)
            ''', (team_id, tournament_id, name, players_json))
            conn.commit()
        return team_id

    def get_teams_by_tournament(self, tournament_id: str) -> List[Dict]:
        """Récupère toutes les équipes d'un tournoi"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM teams
                WHERE tournament_id = ?
                ORDER BY name
            ''', (tournament_id,))
            rows = cursor.fetchall()

            teams = []
            for row in rows:
                team = dict(row)
                team['players'] = json.loads(team['players']) if team['players'] else []
                teams.append(team)
            return teams

    def update_team_stats(
        self,
        team_id: str,
        wins: int = None,
        losses: int = None,
        points_for: int = None,
        points_against: int = None,
    ):
        """Met à jour les statistiques d'une équipe"""
        updates = {}
        if wins is not None:
            updates['wins'] = wins
        if losses is not None:
            updates['losses'] = losses
        if points_for is not None:
            updates['points_for'] = points_for
        if points_against is not None:
            updates['points_against'] = points_against

        if updates:
            set_clause = ', '.join([f"{key} = ?" for key in updates.keys()])
            values = list(updates.values()) + [team_id]

            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f'''
                    UPDATE teams SET {set_clause} WHERE id = ?
                ''', values)
                conn.commit()

    def update_team(
        self,
        team_id: str,
        name: Optional[str] = None,
        players: Optional[List[str]] = None
    ):
        """Met à jour le nom et/ou la liste des joueurs d'une équipe"""
        updates = {}
        if name is not None:
            updates['name'] = name
        if players is not None:
            updates['players'] = json.dumps(players)

        if not updates:
            return

        set_clause = ', '.join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values()) + [team_id]

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE teams SET {set_clause} WHERE id = ?",
                values
            )
            conn.commit()

    def delete_team(self, team_id: str):
        """Supprime une équipe et ses matchs associés"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM matches WHERE team1_id = ? OR team2_id = ?',
                (team_id, team_id)
            )
            cursor.execute('DELETE FROM teams WHERE id = ?', (team_id,))
            conn.commit()

    # CRUD pour Matchs
    def create_match(
        self,
        tournament_id: str,
        round_number: int,
        team1_id: str,
        team2_id: str,
        court_number: int = None
    ) -> str:
        """Crée un nouveau match"""
        match_id = str(uuid.uuid4())

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO matches (id, tournament_id, round_number, team1_id, team2_id, court_number)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (match_id, tournament_id, round_number, team1_id, team2_id, court_number))
            conn.commit()
        return match_id

    def get_matches_by_tournament_round(self, tournament_id: str, round_number: int) -> List[Dict]:
        """Récupère tous les matchs d'un tournoi pour un tour donné"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT m.*, 
                       t1.name as team1_name, t2.name as team2_name
                FROM matches m
                JOIN teams t1 ON m.team1_id = t1.id
                JOIN teams t2 ON m.team2_id = t2.id
                WHERE m.tournament_id = ? AND m.round_number = ?
                ORDER BY m.court_number
            ''', (tournament_id, round_number))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def update_match_score(self, match_id: str, team1_score: int, team2_score: int):
        """Met à jour le score d'un match"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE matches
                SET team1_score = ?, team2_score = ?, status = 'finished'
                WHERE id = ?
            ''', (team1_score, team2_score, match_id))
            conn.commit()

    def update_match_court(self, match_id: str, court_number: int):
        """Met à jour le numéro de terrain d'un match"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE matches SET court_number = ? WHERE id = ?',
                (court_number, match_id)
            )
            conn.commit()

    def delete_match(self, match_id: str):
        """Supprime un match"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM matches WHERE id = ?', (match_id,))
            conn.commit()

    def get_team_standings(self, tournament_id: str) -> List[Dict]:
        """Calcule et retourne le classement des équipes"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT t.id, t.name, t.wins, t.losses, t.points_for, t.points_against,
                       (t.points_for - t.points_against) as point_difference
                FROM teams t
                WHERE t.tournament_id = ?
                ORDER BY t.wins DESC, point_difference DESC, t.points_for DESC
            ''', (tournament_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

# Instance globale du gestionnaire de base de données
db_manager = DatabaseManager()
