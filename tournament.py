"""
Module de logique de tournoi pour Pétanque Manager
Gère les algorithmes d'appariement et la génération des tours
"""

import random
from typing import List, Dict, Tuple, Optional
from store import db_manager

class TournamentManager:
    """Gestionnaire de la logique de tournoi"""
    
    def __init__(self):
        pass
    
    def generate_next_round(self, tournament_id: str) -> List[Dict]:
        """Génère le tour suivant pour un tournoi"""
        tournament = db_manager.get_tournament(tournament_id)
        if not tournament:
            raise ValueError("Tournoi introuvable")
        
        tournament_type = tournament['type']
        current_round = tournament['current_round']
        next_round = current_round + 1
        
        # Récupérer les équipes et leurs statistiques
        teams = db_manager.get_teams_by_tournament(tournament_id)
        if len(teams) < 2:
            raise ValueError("Au moins 2 équipes sont nécessaires")
        
        # Générer les matchs selon le type de tournoi
        if tournament_type in ['tete_a_tete', 'doublette', 'triplette']:
            matches = self._generate_standard_matches(tournament_id, teams, next_round, tournament['num_courts'])
        elif tournament_type == 'quadrette':
            matches = self._generate_quadrette_matches(tournament_id, teams, next_round, tournament['num_courts'])
        elif tournament_type == 'melee':
            matches = self._generate_melee_matches(tournament_id, teams, next_round, tournament['num_courts'])
        else:
            raise ValueError(f"Type de tournoi non supporté: {tournament_type}")
        
        # Mettre à jour le tour actuel
        db_manager.update_tournament(tournament_id, current_round=next_round)
        
        return matches
    
    def _generate_standard_matches(self, tournament_id: str, teams: List[Dict], 
                                 round_number: int, num_courts: int) -> List[Dict]:
        """Génère les matchs pour les tournois standard (tête-à-tête, doublette, triplette)"""
        # Calculer les performances des équipes
        team_performances = []
        for team in teams:
            wins = team.get('wins', 0)
            losses = team.get('losses', 0)
            points_for = team.get('points_for', 0)
            points_against = team.get('points_against', 0)
            
            # Performance = différence de points pondérée par le ratio victoires/défaites
            total_games = wins + losses
            win_ratio = wins / total_games if total_games > 0 else 0
            point_diff = points_for - points_against
            performance = point_diff + (win_ratio * 50)  # Bonus pour les victoires
            
            team_performances.append((team, performance))
        
        # Trier par performance
        team_performances.sort(key=lambda x: x[1], reverse=True)
        
        # Gérer le nombre impair d'équipes (BYE)
        if len(teams) % 2 == 1:
            if round_number == 1:
                # Premier tour : BYE aléatoire
                bye_team = random.choice(teams)
            else:
                # Tours suivants : BYE pour l'équipe la moins bien classée
                bye_team = team_performances[-1][0]
            
            # Créer un match BYE (victoire 13-7)
            bye_match_id = db_manager.create_match(tournament_id, round_number, 
                                                 bye_team['id'], bye_team['id'], None)
            db_manager.update_match_score(bye_match_id, 13, 7)
            
            # Mettre à jour les stats de l'équipe
            self._update_team_stats_after_match(bye_team['id'], 13, 7, bye_team['id'], 13, 7)
            
            # Retirer l'équipe BYE de la liste
            teams = [t for t in teams if t['id'] != bye_team['id']]
            team_performances = [tp for tp in team_performances if tp[0]['id'] != bye_team['id']]
        
        # Apparier les équipes
        matches = []
        used_teams = set()
        court = 1
        
        # Stratégie d'appariement : équipes de performance similaire
        for i in range(0, len(team_performances) - 1, 2):
            if len(used_teams) >= len(teams):
                break
                
            team1 = team_performances[i][0]
            team2 = team_performances[i + 1][0]
            
            if team1['id'] not in used_teams and team2['id'] not in used_teams:
                # Vérifier qu'ils ne se sont pas déjà rencontrés
                if not self._have_teams_played(tournament_id, team1['id'], team2['id']):
                    match_id = db_manager.create_match(tournament_id, round_number,
                                                     team1['id'], team2['id'], court)
                    matches.append({
                        'id': match_id,
                        'team1': team1,
                        'team2': team2,
                        'court': court
                    })
                    used_teams.add(team1['id'])
                    used_teams.add(team2['id'])
                    court = (court % num_courts) + 1
        
        return matches
    
    def _generate_quadrette_matches(self, tournament_id: str, teams: List[Dict], 
                                  round_number: int, num_courts: int) -> List[Dict]:
        """Génère les matchs pour les tournois quadrette (planning fixe sur 7 tours)"""
        if round_number > 7:
            raise ValueError("Le tournoi quadrette ne peut avoir plus de 7 tours")
        
        # Planning fixe des 7 tours de quadrette
        round_patterns = {
            1: "ABC vs D",     # Groupe ABC contre joueur D
            2: "AB vs CD",     # AB contre CD
            3: "ABD vs C",     # ABD contre C
            4: "AC vs BD",     # AC contre BD
            5: "ACD vs B",     # ACD contre B
            6: "AD vs BC",     # AD contre BC
            7: "BCD vs A"      # BCD contre A
        }
        
        pattern = round_patterns[round_number]
        matches = []
        court = 1
        
        # Pour chaque équipe de 4 joueurs, créer les sous-équipes selon le pattern
        i = 0
        while i < len(teams) - 1:
            team1 = teams[i]
            team2 = teams[i + 1] if i + 1 < len(teams) else None
            
            if team2 is None:
                break
                
            # Créer le match selon le pattern du tour
            match_id = db_manager.create_match(tournament_id, round_number,
                                             team1['id'], team2['id'], court)
            matches.append({
                'id': match_id,
                'team1': team1,
                'team2': team2,
                'court': court,
                'pattern': pattern
            })
            
            court = (court % num_courts) + 1
            i += 2
        
        return matches
    
    def _generate_melee_matches(self, tournament_id: str, teams: List[Dict], 
                              round_number: int, num_courts: int) -> List[Dict]:
        """Génère les matchs pour les tournois mêlée (tirage aléatoire)"""
        # Mélanger aléatoirement les équipes
        shuffled_teams = teams.copy()
        random.shuffle(shuffled_teams)
        
        matches = []
        court = 1
        
        # Créer des groupes de 2 ou 3 selon le nombre de terrains disponibles
        players_per_court = len(shuffled_teams) // num_courts
        if players_per_court < 2:
            players_per_court = 2
        
        i = 0
        while i < len(shuffled_teams) - 1:
            team1 = shuffled_teams[i]
            team2 = shuffled_teams[i + 1] if i + 1 < len(shuffled_teams) else None
            
            if team2 is None:
                break
                
            match_id = db_manager.create_match(tournament_id, round_number,
                                             team1['id'], team2['id'], court)
            matches.append({
                'id': match_id,
                'team1': team1,
                'team2': team2,
                'court': court
            })
            
            court = (court % num_courts) + 1
            i += 2
        
        return matches
    
    def _have_teams_played(self, tournament_id: str, team1_id: str, team2_id: str) -> bool:
        """Vérifie si deux équipes se sont déjà rencontrées"""
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM matches 
                WHERE tournament_id = ? AND (
                    (team1_id = ? AND team2_id = ?) OR 
                    (team1_id = ? AND team2_id = ?)
                )
            ''', (tournament_id, team1_id, team2_id, team2_id, team1_id))
            count = cursor.fetchone()[0]
            return count > 0
    
    def update_match_result(self, match_id: str, team1_score: int, team2_score: int):
        """Met à jour le résultat d'un match et les statistiques des équipes"""
        # Récupérer les informations du match
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT team1_id, team2_id FROM matches WHERE id = ?', (match_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError("Match introuvable")
            
            team1_id, team2_id = row
        
        # Mettre à jour le score du match
        db_manager.update_match_score(match_id, team1_score, team2_score)
        
        # Mettre à jour les statistiques des équipes
        self._update_team_stats_after_match(team1_id, team1_score, team2_score, 
                                          team2_id, team2_score, team1_score)
    
    def _update_team_stats_after_match(self, team1_id: str, team1_score: int, team2_score: int,
                                     team2_id: str, team2_score_for_team2: int, team1_score_for_team2: int):
        """Met à jour les statistiques des équipes après un match"""
        # Récupérer les stats actuelles des équipes
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Team 1
            cursor.execute('SELECT wins, losses, points_for, points_against FROM teams WHERE id = ?', (team1_id,))
            team1_stats = cursor.fetchone()
            
            # Team 2 
            cursor.execute('SELECT wins, losses, points_for, points_against FROM teams WHERE id = ?', (team2_id,))
            team2_stats = cursor.fetchone()
            
            if not team1_stats or not team2_stats:
                return
            
            # Calcul des nouvelles statistiques
            team1_wins = team1_stats[0]
            team1_losses = team1_stats[1]
            team1_points_for = team1_stats[2] + team1_score
            team1_points_against = team1_stats[3] + team2_score
            
            team2_wins = team2_stats[0]
            team2_losses = team2_stats[1]
            team2_points_for = team2_stats[2] + team2_score_for_team2
            team2_points_against = team2_stats[3] + team1_score_for_team2
            
            # Déterminer le vainqueur
            if team1_score > team2_score:
                team1_wins += 1
                team2_losses += 1
            elif team2_score > team1_score:
                team2_wins += 1
                team1_losses += 1
            # Égalité = pas de changement dans wins/losses
            
            # Mettre à jour les stats
            db_manager.update_team_stats(team1_id, team1_wins, team1_losses, 
                                       team1_points_for, team1_points_against)
            db_manager.update_team_stats(team2_id, team2_wins, team2_losses, 
                                       team2_points_for, team2_points_against)
    
    def get_tournament_status(self, tournament_id: str) -> Dict:
        """Retourne le statut actuel du tournoi"""
        tournament = db_manager.get_tournament(tournament_id)
        if not tournament:
            return {}
        
        teams = db_manager.get_teams_by_tournament(tournament_id)
        current_round = tournament['current_round']
        
        # Récupérer les matchs du tour actuel s'il existe
        current_matches = []
        if current_round > 0:
            current_matches = db_manager.get_matches_by_tournament_round(tournament_id, current_round)
        
        return {
            'tournament': tournament,
            'teams': teams,
            'current_round': current_round,
            'current_matches': current_matches,
            'standings': db_manager.get_team_standings(tournament_id)
        }
